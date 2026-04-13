from __future__ import annotations

import asyncio
import time
from datetime import datetime, timedelta
from typing import Optional
from urllib.parse import urlencode

import httpx

from b1sl.b1sl.base_adapter import BaseRestAdapter, HookContext
from b1sl.b1sl.exceptions.exceptions import (
    B1AuthError,
    B1Exception,
    B1NotFoundError,
    B1ValidationError,
)
from b1sl.b1sl.models.result import Result

_HTTP_STATUS_TO_EXC: dict[int, type] = {
    400: B1ValidationError,
    401: B1AuthError,
    404: B1NotFoundError,
}


class AsyncRestAdapter(BaseRestAdapter):
    """
    Asynchronous HTTP adapter for SAP B1 Service Layer using httpx.

    This adapter provides high-concurrency support with thread-safe (async-safe)
    session management via an internal asyncio.Lock. It handles automatic
    re-authentication and structured logging.

    AI Role: Recommended for FastAPI, Temporal, or bulk async tasks.
    Prevents race conditions when multiple concurrent tasks hit the session.
    """



    def __init__(self, *args, session_id: str | None = None, **kwargs):
        """
        Initializes the async httpx client and session lock.

        Args:
            session_id (str, optional): An existing B1SESSION cookie to reuse.
                Prevents a full login if already authenticated.
        """
        super().__init__(*args, **kwargs)
        self._initial_session_id = session_id
        self._client: httpx.AsyncClient | None = None
        self._lock: asyncio.Lock | None = None

    async def _get_lock(self) -> asyncio.Lock:
        if self._lock is None:
            self._lock = asyncio.Lock()
        return self._lock

    @property
    def session_id(self) -> str | None:
        """
        Retrieves the current SAP session ID from the httpx cookie jar.

        Returns:
            str: The B1SESSION cookie value or None.
        """
        if not self._client:
            return None
        return self._client.cookies.get("B1SESSION")

    async def connect(self) -> None:
        """
        Initializes the underlying HTTP client and logs in.
        Must be called if not using the async context manager.
        """
        if not self._client:
            self._client = httpx.AsyncClient(
                verify=self._ssl_verify,
                timeout=httpx.Timeout(
                    self._connect_timeout,
                    read=self._read_timeout,
                    write=self._read_timeout,
                    pool=self._connect_timeout,
                ),
                follow_redirects=True,
            )
            # Hydrate session if provided
            if self._initial_session_id:
                 self._client.cookies.set("B1SESSION", self._initial_session_id)
                 self.is_session_active = True
                 # We don't have an expiry date, so we set it to None, which
                 # forces the 401-retry logic to handle it if it's already expired.
                 self.token_expiry = None
        self._is_closed = False
        await self.ensure_session()

    async def aclose(self) -> None:
        """
        Logs out and closes the underlying HTTP client pool.
        Must be called to ensure clean shutdown if not using the context manager.
        """
        if getattr(self, "_is_closed", False):
            return

        if self.is_session_active:
            try:
                await self.logout()
            except Exception as e:
                self._logger.warning(
                    f"[{self._username}] Failed to logout during cleanup: {e}"
                )
        if self._client:
            await self._client.aclose()
            self._client = None

        self._is_closed = True

    async def __aenter__(self) -> AsyncRestAdapter:
        """
        Async context manager entry point. Initialises the HTTP client.

        Returns:
            AsyncRestAdapter: The initialised instance.
        """
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Async context manager exit point. Performs logout and closes the client.
        """
        await self.aclose()

    async def ensure_session(self, force_refresh_if_expiry: Optional[datetime] = None, force_refresh: bool = False) -> None:
        """
        Ensures a valid SAP session exists before a request.

        Uses an internal asyncio.Lock to prevent multiple concurrent login
        attempts when many tasks start simultaneously. If force_refresh_if_expiry
        is provided, it will forcefully invalidate the session ONLY if the token
        hasn't been refreshed by another task in the meantime.
        """
        if not self._client:
            raise B1Exception("AsyncRestAdapter not initialized. Call connect() first.")
        lock = await self._get_lock()
        async with lock:
            if (force_refresh or force_refresh_if_expiry is not None) and self.token_expiry == force_refresh_if_expiry:
                self.is_session_active = False

            # We should login if:
            # 1. We are not active (Initial start or logout or forced refresh)
            # 2. We are active but we have an expiry date and it has passed.
            # Note: We DON'T login if we are active but have no expiry (Hydrated session).
            should_login = not self.is_session_active
            if not should_login and self.token_expiry:
                should_login = datetime.now() >= self.token_expiry

            if should_login:
                await self.login()

    async def login(self) -> Result:
        """
        Asynchronously authenticates with the SAP B1 Service Layer.
        """
        data = {
            "UserName": self._username,
            "Password": self._password,
            "CompanyDB": self._db,
        }
        self._logger.info(f"Logging in to SAP B1 at {self.raw_base_url}...")

        try:
            # We call _do which handles its own timing and logging
            return await self._do(
                http_method="POST", endpoint="Login", data=data, _is_login=True
            )
        except Exception as e:
            self._logger.error(f"Login failed: {e}")
            raise B1AuthError(f"Login failed: {e}") from e

    async def logout(self) -> Result:
        """
        Asynchronously releases the SAP B1 session license.

        Returns:
            Result: Current logout state.
        """
        if not self._client:
            return Result(status_code=200, message="Closed")
        try:
            response = await self._client.post(f"{self.raw_base_url}/Logout")
            self.is_session_active = False
            self.token_expiry = None
            return Result(
                status_code=response.status_code, message=response.reason_phrase
            )
        except Exception as e:
            self._logger.warning(f"[{self._username}] Logout failed: {e}")
            return Result(status_code=500, message=str(e))

    @staticmethod
    def _parse_sap_error(response: httpx.Response) -> tuple[str, str]:
        """Parses error information from an Httpx response object."""
        try:
            body = response.json()
        except Exception:
            body = None
        return AsyncRestAdapter._parse_sap_error_shared(
            response.status_code, response.reason_phrase, body
        )

    async def _do(
        self,
        http_method: str,
        endpoint: str,
        ep_params=None,
        data=None,
        _is_login: bool = False,
        _retry_once=True,
    ) -> Result:
        """
        Dispatches an asynchronous HTTP request to SAP SL.
        Implements Senior Observability (Timing + Structured Logging + Async Hooks).
        """
        # Removed redundant imports moved to module level
        if not _is_login:
            await self.ensure_session()

        req_id = self._generate_req_id()
        endpoint_path = endpoint if endpoint.startswith("/") else f"/{endpoint}"
        full_url = self.raw_base_url + endpoint_path

        log_data = self._redact_data(data)
        self._logger.debug(f"[{req_id}] data={log_data}")

        start_time = time.perf_counter()
        exc_captured: Exception | None = None
        response: httpx.Response | None = None
        is_success = False

        try:
            # ── ETag: inject If-None-Match (GET) or If-Match (PATCH/DELETE/POST) ──
            headers = self._build_headers(http_method, endpoint_path)

            if self._dry_run_active and http_method in {"POST", "PATCH", "DELETE"} and not _is_login:
                self._logger.info(f"[{req_id}] [DRY RUN] Intercepting {http_method} {full_url}")
                # We simulate a response object to keep the rest of the logic working (hooks, logs, etc)
                is_success = True
                response = httpx.Response(204, request=httpx.Request(http_method, full_url))
            else:
                response = await self._client.request(
                    method=http_method, url=full_url, params=ep_params, json=data,
                    headers=headers,
                )

            if response.status_code == 401 and _retry_once and not _is_login:
                self._logger.warning(f"[{req_id}] 401 Unauthorized - retrying login...")
                await self.ensure_session(force_refresh_if_expiry=self.token_expiry, force_refresh=True)
                # Recursive call will handle its own finally block,
                # but we need to return here to avoid double-logging/hooking.
                return await self._do(
                    http_method, endpoint, ep_params, data, _is_login, _retry_once=False
                )

            response.raise_for_status()
            is_success = True
        except httpx.HTTPStatusError as e:
            exc_captured = e
            sap_code, sap_msg = self._parse_sap_error(e.response)
            # ── Raise specialised exception before falling back to B1Exception ──
            try:
                body = e.response.json() if e.response.content else None
            except Exception:
                body = None
            self._raise_if_concurrency_error(
                e.response.status_code, sap_code, sap_msg, endpoint_path, body
            )
            raise B1Exception(f"SAP Error {sap_code}: {sap_msg}") from e
        except Exception as e:
            exc_captured = e
            raise B1Exception(f"Request failed: {e}") from e
        finally:
            # Only log/hook if this is not the first attempt of a 401 retry
            if not (
                response is not None
                and response.status_code == 401
                and _retry_once
                and not _is_login
            ):
                duration_ms = (time.perf_counter() - start_time) * 1000
                status_code = response.status_code if response is not None else None

                ctx = HookContext(
                    req_id=req_id,
                    http_method=http_method,
                    base_url=self.raw_base_url,
                    endpoint=endpoint_path,
                    query_params=urlencode(ep_params) if ep_params else "",
                    db=self._db,
                    user=self._username,
                    status_code=status_code,
                    duration_ms=duration_ms,
                    extra=dict(self._obs.context_extras),
                    exc=exc_captured,
                )

                self._log_response(ctx)
                await self._hooks.adispatch(
                    "on_error" if exc_captured else "on_response", ctx, self._logger
                )

        if _is_login and is_success and response is not None:
            data_out = response.json()
            timeout_min = data_out.get("SessionTimeout", 30)
            self.token_expiry = datetime.now() + timedelta(minutes=timeout_min - 2)
            self.is_session_active = True

        if is_success and response is not None:
            data_out = response.json() if response.content else None
            # ── ETag: extract from header (preferred) or body fallback ──
            self._extract_etag(endpoint_path, dict(response.headers), data_out)
            return Result(
                status_code=response.status_code,
                message=response.reason_phrase,
                data=data_out,
                next_link=data_out.get("odata.nextLink")
                if isinstance(data_out, dict)
                else None,
                next_params=self._get_ep_params(data_out.get("odata.nextLink"))
                if isinstance(data_out, dict) and data_out.get("odata.nextLink")
                else None,
                metadata=data_out.get("odata.metadata")
                if isinstance(data_out, dict)
                else None,
            )
        else:
            raise B1Exception(
                f"HTTP Error {response.status_code if response else 'Unknown'}"
            )

    async def get(self, endpoint, ep_params=None, data=None):
        """Execute an asynchronous GET request."""
        return await self._do("GET", endpoint, ep_params, data)

    async def post(self, endpoint, ep_params=None, data=None):
        """Execute an asynchronous POST request."""
        return await self._do("POST", endpoint, ep_params, data)

    async def patch(self, endpoint, ep_params=None, data=None):
        """Execute an asynchronous PATCH request."""
        return await self._do("PATCH", endpoint, ep_params, data)

    async def delete(self, endpoint, ep_params=None, data=None):
        """Execute an asynchronous DELETE request."""
        return await self._do("DELETE", endpoint, ep_params, data)
