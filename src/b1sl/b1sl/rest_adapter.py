from __future__ import annotations

import functools
import threading
import time
from datetime import datetime, timedelta
from urllib.parse import urlencode, urlsplit

import httpx

from b1sl.b1sl.base_adapter import BaseRestAdapter, HookContext
from b1sl.b1sl.exceptions.exceptions import (
    B1AuthError,
    B1ConnectionError,
    B1Exception,
    B1NotFoundError,
    B1ValidationError,
    SAPConcurrencyError,
)
from b1sl.b1sl.models.result import Result
from b1sl.b1sl.pagination import extract_next_link

_HTTP_STATUS_TO_EXC: dict[int, type] = {
    400: B1ValidationError,
    401: B1AuthError,
    404: B1NotFoundError,
    # 412 with SAP code -2039 raises earlier via _raise_if_concurrency_error
    # (richer context); this entry guarantees the semantic type either way.
    412: SAPConcurrencyError,
}


class RestAdapter(BaseRestAdapter):
    """
    Synchronous HTTP adapter for SAP B1 Service Layer using requests.

    This adapter manages session lifecycle (login/logout), re-authentication
    on 401 errors, and ETag-based optimistic concurrency for single-threaded
    or WSGI environments. It uses httpx.Client for parity with the async client.

    AI Role: Use for synchronous workflows or legacy integrations.
    Handles basic CRUD operations and session resilience automatically.
    """



    def __init__(self, *args, session_id: str | None = None, **kwargs):
        """
        Initializes the synchronous httpx client.

        Args:
            session_id (str, optional): An existing B1SESSION cookie to reuse.
                Prevents a full login if already authenticated (parity with
                AsyncRestAdapter hydration). A session ID is a
                bearer-credential equivalent — treat it like a password.
        """
        super().__init__(*args, **kwargs)
        self._lock = threading.Lock()
        self.session = httpx.Client(
            verify=self._ssl_verify,
            timeout=httpx.Timeout(
                self._connect_timeout,
                read=self._read_timeout,
                write=self._read_timeout,
                pool=self._connect_timeout,
            ),
            follow_redirects=True,
        )
        if session_id:
            # Scope the hydrated cookie to the SAP host so it can never be
            # sent to another domain (e.g. via a cross-host redirect).
            self.session.cookies.set(
                "B1SESSION",
                session_id,
                domain=urlsplit(self.raw_base_url).hostname or "",
            )
            self.is_session_active = True
            # No known expiry: the 401-retry logic recovers if it is stale.
            # _is_token_expire() treats expiry=None as "needs login", so give
            # the hydrated session a far-future expiry to avoid an eager login.
            self.token_expiry = datetime.max

    def close(self) -> None:
        """
        Logs out and closes the underlying HTTP client pool.

        Logging out releases the SAP session license immediately instead of
        holding it until the server-side timeout. Mirrors ``AsyncRestAdapter.aclose()``.
        """
        if getattr(self, "_is_closed", False):
            return

        if self.is_session_active:
            try:
                self._logout()
            except Exception as e:
                self._logger.warning(
                    f"[{self._username}] Failed to logout during cleanup: {e}"
                )
        if self.session:
            self.session.close()

        self._is_closed = True

    @property
    def session_id(self) -> str | None:
        """
        Retrieves the current SAP session ID from the cookie jar.

        Returns:
            str: The B1SESSION cookie value or None.
        """
        return self.session.cookies.get("B1SESSION")

    @staticmethod
    def handle_token(manage_token: bool = True):
        """
        Decorator for methods requiring a valid SAP session.

        Logs in before the method call if needed and potentially logs out
        afterwards depending on the reuse_token configuration.

        Args:
            manage_token (bool): Whether to perform session lifecycle management.
        """

        def decorator(func):
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                if manage_token:
                    self._handle_token_login()
                try:
                    result = func(self, *args, **kwargs)
                finally:
                    if manage_token:
                        self._handle_token_logout()
                return result

            return wrapper

        return decorator

    def login(self):
        """Authenticate with the SAP B1 Service Layer."""
        return self._login()

    def logout(self):
        """Release the SAP B1 session license."""
        return self._logout()

    def _login(self):
        """
        Internal login implementation.

        Calls POST /Login and updates session state and expiry.

        Returns:
            Result: Response from the Login endpoint.
        """
        data = {
            "UserName": self._username,
            "Password": self._password,
            "CompanyDB": self._db,
        }
        self._logger.info(f"Logging in to SAP B1 at {self.raw_base_url}...")

        try:
            response = self._do(
                http_method="POST", endpoint="/Login", data=data, _is_login=True
            )
        except Exception as e:
            self._logger.error(f"Login failed: {e}")
            raise B1AuthError(f"Login failed: {e}") from e
        if response.status_code == 200:
            self.is_session_active = True
            fallback_min = self.token_timeout.total_seconds() / 60
            timeout_min = response.data.get("SessionTimeout", fallback_min)
            self.token_expiry = datetime.now() + timedelta(minutes=timeout_min - 2)
        return response

    def _logout(self):
        """
        Internal logout implementation.

        Never raises (parity with AsyncRestAdapter.logout): a failed logout
        is logged and reported as a Result(500).

        Returns:
            Result: Response from the Logout endpoint.
        """
        try:
            response = self._do(http_method="POST", endpoint="/Logout", _is_login=True)
            self.is_session_active = False
            self.token_expiry = None
            return response
        except Exception as e:
            self._logger.warning(f"[{self._username}] Logout failed: {e}")
            return Result(status_code=500, message=str(e))

    def _is_token_expire(self) -> bool:
        """
        Checks if the current session token is missing or expired.

        Returns:
            bool: True if a new login is required.
        """
        return self.token_expiry is None or datetime.now() >= self.token_expiry

    def _handle_token_login(self):
        """Standard login handler used by the decorator."""
        if self.reuse_token:
            if self._is_token_expire():
                with self._lock:
                    if self._is_token_expire():
                        self._login()
        else:
            with self._lock:
                self._login()

    def _handle_token_logout(self):
        """Standard logout handler used by the decorator."""
        if not self.reuse_token:
            self._logout()

    def _get_full_url(self, next_link: str) -> str:
        """Normalizes a nextLink to a relative resource path."""
        return "/" + urlsplit(next_link).path.lstrip("/")

    def _process_next_link(self, next_link: str) -> tuple[str, str, dict]:
        """Parses an OData nextLink for multi-page results."""
        return (
            self._clean_url(next_link),
            self._get_full_url(next_link),
            self._get_ep_params(next_link),
        )

    @staticmethod
    def _parse_sap_error(response: httpx.Response) -> tuple[str, str]:
        """Parses error information from an Httpx response object."""
        try:
            body = response.json()
        except Exception:
            body = None
        return RestAdapter._parse_sap_error_shared(response.status_code, response.reason_phrase, body)

    def _execute_request(
        self,
        http_method: str,
        full_url: str,
        headers: dict,
        ep_params: dict | None,
        data: dict | None,
    ) -> httpx.Response:
        """Executes the raw HTTP request using the httpx client."""
        return self.session.request(
            method=http_method,
            url=full_url,
            headers=headers,
            params=ep_params,
            json=data,
        )

    def _do(
        self,
        http_method: str,
        endpoint: str,
        ep_params: dict | None = None,
        data: dict | None = None,
        headers: dict | None = None,
        _is_login: bool = False,
        _retry_once: bool = True,
    ) -> Result:
        """
        Dispatches a standardized HTTP request to SAP.
        Implements Senior Observability (Timing + Structured Logging + Hooks).
        """
        # Removed redundant imports moved to module level
        req_id = self._generate_req_id()
        endpoint_path = endpoint if endpoint.startswith("/") else f"/{endpoint}"
        full_url = self.raw_base_url + endpoint_path

        # ── ETag: inject If-None-Match (GET) or If-Match (PATCH/DELETE/POST) ──
        req_headers = self._build_headers(http_method, endpoint_path)
        if headers:
            req_headers.update(headers)

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
            if is_dry_run:
                self._logger.info(f"[{req_id}] [DRY RUN] Intercepting {http_method} {full_url}")
                is_success = True
                response = httpx.Response(204, request=httpx.Request(http_method, full_url))
            else:
                response = self._execute_request(
                    http_method, full_url, req_headers, ep_params, data
                )

            if response.status_code == 401 and _retry_once and not _is_login:
                self._logger.warning(f"[{req_id}] 401 Unauthorized - retrying login...")
                old_token_expiry = self.token_expiry
                with self._lock:
                    if self.token_expiry == old_token_expiry:
                        self._login()
                # Recursive call maps its own errors to semantic exceptions
                # (404 → B1NotFoundError, 412 → SAPConcurrencyError, …) and
                # handles its own logging/hooks, mirroring the async adapter.
                return self._do(
                    http_method, endpoint, ep_params, data, headers, _is_login, _retry_once=False
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
                self._hooks.dispatch(
                    "on_error" if exc_captured else "on_response", ctx, self._logger
                )

        if is_success and response is not None:
            # ── ETag: proactively drop stale entries after a real write ──
            if http_method in {"PATCH", "DELETE", "POST"} and not _is_login and not is_dry_run:
                self._invalidate_etag_after_write(endpoint_path, dict(response.headers))
            if response.content:
                try:
                    data_out = response.json()
                except Exception:
                    # Non-JSON success body — e.g. ``GET <Entity>/$count`` returns
                    # a bare text/plain integer in OData v4. Return the raw text.
                    self._extract_etag(endpoint_path, dict(response.headers), None)
                    return Result(
                        status_code=response.status_code,
                        message=response.reason_phrase,
                        data=response.text,
                    )
                is_dict = isinstance(data_out, dict)
                # ── ETag: extract from header (preferred) or body fallback ──
                self._extract_etag(
                    endpoint_path, dict(response.headers), data_out if is_dict else None
                )
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
                )
            else:
                self._extract_etag(endpoint_path, dict(response.headers), None)
                return Result(
                    status_code=response.status_code, message=response.reason_phrase, data=None
                )
        else:
            raise B1Exception(
                f"HTTP Error {response.status_code if response else 'Unknown'}"
            )

    @handle_token()
    def get(self, endpoint, ep_params=None, data=None, headers=None):
        """Execute a synchronous GET request."""
        return self._do("GET", endpoint, ep_params, data, headers=headers)

    @handle_token()
    def post(self, endpoint, ep_params=None, data=None, headers=None):
        """Execute a synchronous POST request."""
        return self._do("POST", endpoint, ep_params, data, headers=headers)

    @handle_token()
    def patch(self, endpoint, ep_params=None, data=None, headers=None):
        """Execute a synchronous PATCH request."""
        return self._do("PATCH", endpoint, ep_params, data, headers=headers)

    @handle_token()
    def delete(self, endpoint, ep_params=None, data=None, headers=None):
        """Execute a synchronous DELETE request."""
        return self._do("DELETE", endpoint, ep_params, data, headers=headers)

    def post_batch(
        self, body: str, headers: dict, _retry_once: bool = True
    ) -> httpx.Response:
        """
        Special method to send raw multipart content for $batch operations.

        Failures of the $batch request itself go through the same semantic
        exception mapping as regular requests (401 → re-login retry,
        404 → B1NotFoundError, etc.). Per-part failures inside a successful
        batch never raise — they surface via BatchResults.
        """
        self._handle_token_login()
        url = f"{self.raw_base_url}/$batch"
        # Combine with session headers if necessary,
        # although httpx already handles them via cookies.
        response = self.session.post(url, content=body, headers=headers)

        if response.status_code == 401 and _retry_once:
            self._logger.warning("401 Unauthorized on $batch - retrying login...")
            old_token_expiry = self.token_expiry
            with self._lock:
                if self.token_expiry == old_token_expiry:
                    self._login()
            return self.post_batch(body, headers, _retry_once=False)

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            sap_code, sap_msg = self._parse_sap_error(e.response)
            try:
                err_body = e.response.json() if e.response.content else None
            except Exception:
                err_body = None
            exc_cls = _HTTP_STATUS_TO_EXC.get(e.response.status_code, B1Exception)
            raise exc_cls(f"SAP Error {sap_code}: {sap_msg}", details=err_body) from e
        return response
