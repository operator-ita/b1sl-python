from __future__ import annotations

import asyncio
import time
from collections.abc import Sequence
from datetime import datetime, timedelta
from typing import Optional
from urllib.parse import urlencode, urlsplit

import httpx

from b1sl.b1sl.base_adapter import _HTTP_STATUS_TO_EXC, BaseRestAdapter, HookContext
from b1sl.b1sl.exceptions.exceptions import (
    B1AuthError,
    B1ConnectionError,
    B1Exception,
)
from b1sl.b1sl.models.multipart import MultipartFile
from b1sl.b1sl.models.result import Result
from b1sl.b1sl.pagination import extract_next_link, extract_odata_count


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
                Prevents a full login if already authenticated. A session ID
                is a bearer-credential equivalent — treat it like a password.
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
            # Hydrate session if provided. Scope the cookie to the SAP host
            # so it can never be sent to another domain (e.g. via a
            # cross-host redirect).
            if self._initial_session_id:
                 self._client.cookies.set(
                     "B1SESSION",
                     self._initial_session_id,
                     domain=urlsplit(self.raw_base_url).hostname or "",
                 )
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

    async def _do(
        self,
        http_method: str,
        endpoint: str,
        ep_params=None,
        data=None,
        headers: dict | None = None,
        _is_login: bool = False,
        _retry_once=True,
        files: list | None = None,
        raw_response: bool = False,
    ) -> Result:
        """
        Dispatches an asynchronous HTTP request to SAP SL.
        Implements Senior Observability (Timing + Structured Logging + Async Hooks).

        ``files`` sends a ``multipart/form-data`` body instead of JSON;
        ``raw_response`` returns the body as untouched bytes in ``Result.data``
        (no JSON decoding, no ETag caching). Both modes keep the full pipeline:
        dry-run, 401 re-login retry, semantic errors, logging and hooks.
        """
        if not _is_login:
            await self.ensure_session()
        if self._client is None:
            raise B1Exception("AsyncRestAdapter not initialized. Call connect() first.")

        req_id = self._generate_req_id()
        endpoint_path = endpoint if endpoint.startswith("/") else f"/{endpoint}"
        full_url = self.raw_base_url + endpoint_path

        log_data = self._redact_data(data)
        self._logger.debug(f"[{req_id}] data={log_data}")

        start_time = time.perf_counter()
        exc_captured: Exception | None = None
        response: httpx.Response | None = None
        is_success = False

        is_dry_run = (
            self._dry_run_active
            and http_method in {"POST", "PATCH", "DELETE"}
            and not _is_login
        )

        try:
            # ── ETag: inject If-None-Match (GET) or If-Match (PATCH/DELETE/POST) ──
            req_headers = self._build_headers(http_method, endpoint_path)
            if headers:
                req_headers.update(headers)
            if files is not None:
                # httpx must own Content-Type so the boundary matches the body,
                # and multipart carries no concurrency semantics — mirror $batch
                # and never send If-Match. Case-insensitive: caller headers may
                # differ.
                req_headers = {
                    k: v for k, v in req_headers.items()
                    if k.lower() not in {"content-type", "if-match"}
                }
            if raw_response:
                # A cached ETag would turn the read into a 304 with an empty body.
                req_headers = {
                    k: v for k, v in req_headers.items() if k.lower() != "if-none-match"
                }

            if is_dry_run:
                self._logger.info(f"[{req_id}] [DRY RUN] Intercepting {http_method} {full_url}")
                # We simulate a response object to keep the rest of the logic working (hooks, logs, etc)
                is_success = True
                response = httpx.Response(204, request=httpx.Request(http_method, full_url))
            else:
                response = await self._client.request(
                    method=http_method, url=full_url, params=ep_params, json=data,
                    files=files, headers=req_headers,
                )

            if response.status_code == 401 and _retry_once and not _is_login:
                self._logger.warning(f"[{req_id}] 401 Unauthorized - retrying login...")
                await self.ensure_session(force_refresh_if_expiry=self.token_expiry, force_refresh=True)
                # Recursive call will handle its own finally block,
                # but we need to return here to avoid double-logging/hooking.
                return await self._do(
                    http_method, endpoint, ep_params, data, headers, _is_login,
                    _retry_once=False, files=files, raw_response=raw_response,
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
            self._raise_if_sql_error(
                e.response.status_code, sap_code, sap_msg, body
            )

            # Use specialized exception based on status code if available
            exc_cls = _HTTP_STATUS_TO_EXC.get(e.response.status_code, B1Exception)
            raise exc_cls(f"SAP Error {sap_code}: {sap_msg}", details=body) from e
        except B1Exception as e:
            # Already semantic (e.g. raised by the recursive 401-retry call or
            # by the re-login itself) — propagate without re-wrapping.
            exc_captured = e
            raise
        except httpx.RemoteProtocolError as e:
            # Stale server-closed keepalive: "Server disconnected without sending
            # a response." httpcore's transport `retries` does NOT cover this (it
            # only retries connection establishment), so handle it here. Safe to
            # retry only for idempotent reads — a non-GET may have reached the
            # server. httpcore evicts the dead connection from the pool, so the
            # retry gets a fresh one automatically.
            exc_captured = e
            if http_method == "GET" and _retry_once and not _is_login:
                self._logger.warning(f"[{req_id}] Stale connection - retrying GET once...")
                return await self._do(
                    http_method, endpoint, ep_params, data, headers, _is_login,
                    _retry_once=False, files=files, raw_response=raw_response,
                )
            raise B1ConnectionError(f"Cannot reach SAP B1: {e}") from e
        except (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError) as e:
            exc_captured = e
            raise B1ConnectionError(f"Cannot reach SAP B1: {e}") from e
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

                # Prepare context extras
                context_extras = dict(self._obs.context_extras)
                context_extras["is_dry_run"] = is_dry_run

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
                    payload=log_data if http_method in {"POST", "PATCH"} else None,
                    if_match=req_headers.get("If-Match"),
                    extra=context_extras,
                    exc=exc_captured,
                )

                self._log_response(ctx)
                await self._hooks.adispatch(
                    "on_error" if exc_captured else "on_response", ctx, self._logger
                )

        if _is_login and is_success and response is not None:
            data_out = response.json()
            fallback_min = self.token_timeout.total_seconds() / 60
            timeout_min = data_out.get("SessionTimeout", fallback_min)
            self.token_expiry = datetime.now() + timedelta(minutes=timeout_min - 2)
            self.is_session_active = True

        if is_success and response is not None:
            # ── ETag: proactively drop stale entries after a real write ──
            if http_method in {"PATCH", "DELETE", "POST"} and not _is_login and not is_dry_run:
                self._invalidate_etag_after_write(endpoint_path, dict(response.headers))
            if raw_response:
                # Binary body: no JSON decoding, and never touch the ETag
                # cache — a $value read is a file fetch, not a concurrency
                # basis.
                return Result(
                    status_code=response.status_code,
                    message=response.reason_phrase,
                    data=response.content,
                )
            if response.content:
                try:
                    data_out = response.json()
                except Exception:
                    # Non-JSON success body — e.g. ``GET <Entity>/$count`` returns
                    # a bare text/plain integer in OData v4. Return the raw text.
                    data_out = response.text
            else:
                data_out = None
            # ── ETag: extract from header (preferred) or body fallback ──
            # $select responses carry a bogus body @odata.etag (see
            # _extract_etag docstring) — only the header is trusted there.
            self._extract_etag(
                endpoint_path,
                dict(response.headers),
                data_out if isinstance(data_out, dict) else None,
                trust_body="$select" not in (ep_params or {}),
            )
            is_dict = isinstance(data_out, dict)
            _next_link = extract_next_link(data_out) if is_dict else None
            return Result(
                status_code=response.status_code,
                message=response.reason_phrase,
                data=data_out,
                next_link=_next_link,
                next_params=self._get_ep_params(_next_link) if _next_link else None,
                metadata=(data_out.get("@odata.context") or data_out.get("odata.metadata"))
                if is_dict
                else None,
                total_count=extract_odata_count(data_out) if is_dict else None,
            )
        else:
            raise B1Exception(
                f"HTTP Error {response.status_code if response else 'Unknown'}"
            )

    async def _request(
        self,
        http_method: str,
        endpoint,
        ep_params=None,
        data=None,
        headers=None,
        files: list | None = None,
        raw_response: bool = False,
    ):
        """Run one public request, honouring per-request logout (reuse_token=False).

        Parity with the sync adapter's ``handle_token`` decorator: when
        ``reuse_token`` is False the session license is released after every
        request instead of being held between calls.
        """
        try:
            return await self._do(
                http_method, endpoint, ep_params, data, headers=headers,
                files=files, raw_response=raw_response,
            )
        finally:
            if not self.reuse_token:
                await self.logout()

    async def get(self, endpoint, ep_params=None, data=None, headers=None):
        """Execute an asynchronous GET request."""
        return await self._request("GET", endpoint, ep_params, data, headers=headers)

    async def post(self, endpoint, ep_params=None, data=None, headers=None):
        """Execute an asynchronous POST request."""
        return await self._request("POST", endpoint, ep_params, data, headers=headers)

    async def patch(self, endpoint, ep_params=None, data=None, headers=None):
        """Execute an asynchronous PATCH request."""
        return await self._request("PATCH", endpoint, ep_params, data, headers=headers)

    async def delete(self, endpoint, ep_params=None, data=None, headers=None):
        """Execute an asynchronous DELETE request."""
        return await self._request("DELETE", endpoint, ep_params, data, headers=headers)

    async def post_batch(
        self, body: str, headers: dict, _retry_once: bool = True
    ) -> httpx.Response:
        """
        Special method to send raw multipart content for $batch operations.

        Failures of the $batch request itself go through the same semantic
        exception mapping as regular requests (401 → re-login retry,
        404 → B1NotFoundError, etc.). Per-part failures inside a successful
        batch never raise — they surface via BatchResults.
        """
        try:
            await self.ensure_session()
            if not self._client:
                 raise B1Exception("AsyncRestAdapter not initialized.")

            url = f"{self.raw_base_url}/$batch"
            # Combine with session headers if necessary,
            # although httpx already handles them via cookies.
            response = await self._client.post(url, content=body, headers=headers)

            if response.status_code == 401 and _retry_once:
                self._logger.warning("401 Unauthorized on $batch - retrying login...")
                await self.ensure_session(
                    force_refresh_if_expiry=self.token_expiry, force_refresh=True
                )
                return await self.post_batch(body, headers, _retry_once=False)

            self._raise_for_sap_status(response)
            return response
        finally:
            # Release the per-request session (reuse_token=False), mirroring
            # _request(). Guarded by _retry_once so the 401-retry recursion
            # does not release the session twice.
            if _retry_once and not self.reuse_token:
                await self.logout()

    async def post_multipart(
        self,
        endpoint: str,
        files: Sequence[MultipartFile],
        headers: dict | None = None,
    ) -> Result:
        """POST ``multipart/form-data`` to any Service Layer endpoint.

        The file-upload escape hatch: ``post()`` and the typed builder only
        speak JSON, while SAP's file endpoints require a multipart body. Goes
        through ``_do()``'s full pipeline: session lifecycle, dry-run, 401
        re-login retry, semantic error mapping, logging and hooks. ``If-Match``
        is never sent (multipart has no concurrency semantics, mirroring
        ``$batch``) and ``Content-Type`` is always left to httpx, which owns
        the multipart boundary.

        Args:
            endpoint: Relative Service Layer path, e.g. ``"Attachments2"``.
            files: File parts to send. One request may carry several.
            headers: Extra headers.

        Returns:
            Result: the parsed JSON body SAP returns (for ``Attachments2``, the
            created entry including its ``AbsoluteEntry``).

        Raises:
            ValueError: if ``files`` is empty.
        """
        if not files:
            raise ValueError("post_multipart() requires at least one file.")
        parts = [f.as_httpx_tuple() for f in files]
        return await self._request("POST", endpoint, headers=headers, files=parts)

    async def get_binary(
        self,
        endpoint: str,
        ep_params: dict | None = None,
        headers: dict | None = None,
    ) -> bytes:
        """GET a raw binary body, with no JSON/text decoding.

        The download counterpart of ``post_multipart``. ``get()`` routes every
        body through ``response.json()`` with a ``response.text`` fallback,
        which corrupts binary payloads — this returns the body bytes untouched.
        Goes through ``_do()``'s full pipeline (session lifecycle, retries,
        semantic errors, logging and hooks), but the ETag cache is never
        touched and ``If-None-Match`` is never sent — a cached ETag would turn
        the read into a 304 with an empty body.

        Args:
            endpoint: Relative path including any key and suffix, e.g.
                ``"Attachments2(12)/$value"``.
            ep_params: Query parameters (e.g. ``{"filename": "'invoice.pdf'"}``).
            headers: Extra headers.

        Returns:
            The response body as raw bytes.
        """
        result = await self._request(
            "GET", endpoint, ep_params, headers=headers, raw_response=True
        )
        data = result.data
        return data if isinstance(data, bytes) else b""
