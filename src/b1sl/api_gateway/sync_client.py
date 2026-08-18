"""
b1sl.api_gateway.sync_client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sync client for the SAP Business One **API Gateway** — the native service
(``sbo-api-gateway-service.jar``, port ``60000`` by default) that exposes
Crystal Reports layouts over REST and renders them to PDF.

It is *not* the Service Layer: different port, ``/rs/v1/`` path, its own
cookie session and its own SAP authorization (*Report Layout API*). This
client therefore shares ``b1sl``'s configuration/observability/exception
building blocks but does **not** inherit from the Service Layer adapter —
the response semantics are incompatible (errors arrive as ``200 OK`` with
sentinel bodies, exports are base64 text, not OData JSON).

Four endpoints::

    POST /login                              → session cookies
    GET  /rs/v1/LoadAuthorizedCRList         → catalog reports (RCRI00xx)
    GET  /rs/v1/LoadCR?DocCode=<code>        → parameter definitions
    POST /rs/v1/ExportPDFData?DocCode=<code> → base64 PDF

Usage::

    from b1sl.api_gateway import APIGatewayClient, APIGatewayConfig

    cfg = APIGatewayConfig.from_env()          # B1SL_GATEWAY_BASE_URL + creds
    with APIGatewayClient(cfg) as gw:
        pdf = gw.export_document_pdf("QUT20020", doc_entry=12345)
        assert pdf.startswith(b"%PDF-")

The async twin is :class:`b1sl.api_gateway.client.AsyncAPIGatewayClient`;
both expose the same members and signatures (enforced by
``tests/unit/test_sync_async_parity.py``).
See ``docs/20-api-gateway.md`` for the full behaviour catalogue.
"""

from __future__ import annotations

import threading
import time
from collections.abc import Mapping, Sequence
from contextlib import AbstractContextManager, nullcontext
from typing import Any
from urllib.parse import urlencode

import httpx

from b1sl.api_gateway._base import (
    LOGIN_PATH,
    LOGOUT_PATH,
    BaseAPIGatewayClient,
    body_details,
    decode_pdf,
    error_envelope,
    is_session_lost,
    parse_parameters,
    parse_report_list,
    req_id,
    snippet,
)
from b1sl.api_gateway.exceptions import (
    APIGatewayAuthError,
    APIGatewayConnectionError,
    APIGatewayError,
    APIGatewayParameterError,
    APIGatewayResponseError,
)
from b1sl.api_gateway.models import ReportInfo, ReportParameter
from b1sl.api_gateway.payload import build_export_payload


class APIGatewayClient(BaseAPIGatewayClient):
    """
    Sync client for the SAP B1 API Gateway (Crystal Reports → PDF).

    Session lifecycle mirrors ``RestAdapter``: ``connect()`` logs in, every
    call goes through ``ensure_session()`` (thread-lock guarded, proactive
    re-login before the reported ``SessionTimeout``), and a session-lost
    status triggers a single re-login + retry. Use as a context manager or
    call ``connect()`` / ``close()`` explicitly. Safe to share between
    threads.

    Args:
        config: Gateway connection settings.
        logger: Defaults to ``b1sl.api_gateway``.
        observability: Same hooks contract as the Service Layer adapters
            (``on_response`` / ``on_error`` receive a ``HookContext``).
    """

    def __init__(self, config, *, logger=None, observability=None) -> None:
        super().__init__(config, logger=logger, observability=observability)
        self._client: httpx.Client | None = None
        self._lock = threading.Lock()
        limit = config.max_concurrent_exports
        self._export_sem: threading.BoundedSemaphore | None = (
            threading.BoundedSemaphore(limit) if limit else None
        )

    # ── Lifecycle ────────────────────────────────────────────────────────── #

    def __enter__(self) -> APIGatewayClient:
        self.connect()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def connect(self) -> None:
        """Create the HTTP client and log in."""
        if self._client is None:
            self._client = httpx.Client(
                verify=self._config.ssl_verify,
                timeout=self._httpx_timeout(),
                # A redirect (e.g. to a login page) must surface as a session
                # problem, never be followed with the cookies attached.
                follow_redirects=False,
            )
        self.ensure_session()

    def close(self) -> None:
        """Log out (best effort) and close the HTTP client."""
        if self._client is None:
            return
        if self.is_session_active:
            self.logout()
        self._client.close()
        self._client = None

    def _export_slot(self) -> AbstractContextManager[Any]:
        """Bound parallel ``ExportPDFData`` calls per ``max_concurrent_exports``."""
        return self._export_sem if self._export_sem is not None else nullcontext()

    def _require_client(self) -> httpx.Client:
        if self._client is None:
            raise APIGatewayError(
                "APIGatewayClient not connected. Use 'with' or call connect() first."
            )
        return self._client

    # ── Session ──────────────────────────────────────────────────────────── #

    def ensure_session(self, *, force_refresh: bool = False) -> None:
        """Log in when there is no session or it is about to expire.

        Serialised with a ``threading.Lock`` so concurrent threads never race
        into multiple logins.
        """
        self._require_client()
        with self._lock:
            if force_refresh:
                self.is_session_active = False
            if self._should_login():
                self.login()

    def login(self) -> dict[str, Any]:
        """``POST /login`` — authenticate and record the session lifetime.

        Returns:
            The login response body (``{"Version": ..., "SessionTimeout": ...}``).

        Raises:
            APIGatewayAuthError: on any non-2xx / non-JSON answer.
            APIGatewayConnectionError: if the host is unreachable.
        """
        client = self._require_client()
        payload = self._login_payload()
        self._logger.info(
            "Logging in to SAP B1 API Gateway at %s (CompanyDB=%s)...",
            self.base_url,
            self._config.company_db,
        )
        rid = req_id()
        started = time.perf_counter()
        response: httpx.Response | None = None
        exc: Exception | None = None
        try:
            response = client.post(self.base_url + LOGIN_PATH, json=payload)
            if response.status_code >= 300:
                raise APIGatewayAuthError(
                    f"API Gateway login failed (HTTP {response.status_code}): "
                    f"{snippet(response)}",
                    details=body_details(response),
                )
            try:
                body = response.json()
            except ValueError as e:
                raise APIGatewayAuthError(
                    f"API Gateway login returned a non-JSON body: {snippet(response)}",
                    details=body_details(response),
                ) from e
            # Bad credentials / unknown CompanyDB come back as HTTP 200 with
            # {"code": -1, "message": {"value": "Failed to login…"}} and no
            # cookie — verified live. Never treat that as a session.
            envelope = error_envelope(body)
            if envelope or "SessionTimeout" not in body:
                raise APIGatewayAuthError(
                    f"API Gateway login rejected: {envelope or snippet(response)}",
                    details=body if isinstance(body, dict) else None,
                )
        except APIGatewayError as e:
            exc = e
            self._forget_session()
            raise
        except (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError) as e:
            exc = e
            self._forget_session()
            raise APIGatewayConnectionError(
                f"Cannot reach SAP B1 API Gateway at {self.base_url}: {e}"
            ) from e
        except httpx.HTTPError as e:
            exc = e
            self._forget_session()
            raise APIGatewayConnectionError(
                f"SAP B1 API Gateway login transport error: {e}"
            ) from e
        finally:
            self._observe(
                rid,
                "POST",
                LOGIN_PATH,
                "",
                response,
                started,
                exc,
                payload={**payload, "Password": "***"},
            )
        return self._record_login(body)

    def logout(self) -> None:
        """``POST /logout`` — best effort; never raises.

        Verified live: the call invalidates the server session (subsequent
        requests get ``401``). Failures are logged at DEBUG and the local
        session state is cleared regardless.
        """
        client = self._client
        self._forget_session()
        if client is None:
            return
        try:
            # The gateway routes /logout through a Spring OIDC handler that
            # answers 415 to a bodiless POST yet still invalidates the
            # session; a JSON body keeps the exchange clean.
            client.post(self.base_url + LOGOUT_PATH, json={})
        except Exception as e:  # pragma: no cover - best effort
            self._logger.debug("API Gateway logout failed (ignored): %s", e)
        finally:
            client.cookies.clear()

    # ── Transport ────────────────────────────────────────────────────────── #

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Any = None,
        _retry_once: bool = True,
    ) -> httpx.Response:
        """One authenticated request under ``/rs/v1``.

        Handles session lifecycle, one re-login retry on a session-lost
        status, network error mapping, logging and hooks. Body-level error
        signals are the caller's job (they differ per endpoint).
        """
        self.ensure_session()
        client = self._require_client()
        endpoint = self._endpoint(path)
        url = self.base_url + endpoint
        rid = req_id()
        started = time.perf_counter()
        response: httpx.Response | None = None
        exc: Exception | None = None
        retrying = False
        try:
            response = client.request(method, url, params=params, json=json)
            if _retry_once and is_session_lost(response.status_code):
                retrying = True
                self._logger.warning(
                    "[%s] HTTP %s from API Gateway - re-login and retry once...",
                    rid,
                    response.status_code,
                )
                self.ensure_session(force_refresh=True)
                return self._request(
                    method, path, params=params, json=json, _retry_once=False
                )
            if is_session_lost(response.status_code):
                raise APIGatewayAuthError(
                    f"API Gateway rejected the request (HTTP {response.status_code}) "
                    "after re-login. Check the user's 'Report Layout API' "
                    f"authorization. {snippet(response)}",
                    details=body_details(response),
                )
            if response.status_code >= 300:
                raise APIGatewayResponseError(
                    f"API Gateway HTTP {response.status_code} on {endpoint}: "
                    f"{snippet(response)}",
                    details=body_details(response),
                )
            return response
        except APIGatewayError as e:
            exc = e
            raise
        except (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError) as e:
            exc = e
            raise APIGatewayConnectionError(
                f"Cannot reach SAP B1 API Gateway at {self.base_url}: {e}"
            ) from e
        except httpx.HTTPError as e:
            exc = e
            raise APIGatewayConnectionError(
                f"SAP B1 API Gateway transport error on {endpoint}: {e}"
            ) from e
        finally:
            if not retrying:
                self._observe(
                    rid,
                    method,
                    endpoint,
                    urlencode(dict(params or {})),
                    response,
                    started,
                    exc,
                    payload=json,
                )

    def _observe(
        self, rid, method, endpoint, query, response, started, exc, *, payload=None
    ) -> None:
        ctx = self._make_ctx(
            rid, method, endpoint, query, response, started, exc, payload
        )
        self._log_ctx(ctx)
        self._hooks.dispatch("on_error" if exc else "on_response", ctx, self._logger)

    # ── Endpoints ────────────────────────────────────────────────────────── #

    def list_reports(self) -> list[ReportInfo]:
        """``GET LoadAuthorizedCRList`` — general-catalog reports (``RCRI00xx``).

        Document-bound print layouts are **not** included; SAP offers no
        endpoint that lists them.
        """
        return parse_report_list(self._request("GET", "LoadAuthorizedCRList"))

    def get_report_parameters(self, doc_code: str) -> list[ReportParameter]:
        """``GET LoadCR?DocCode=…`` — the layout's parameter definitions.

        Raises:
            APIGatewayLayoutNotFoundError: the gateway answered ``{}`` — the
                ``DocCode`` does not exist (no 404 is ever sent).
        """
        response = self._request("GET", "LoadCR", params={"DocCode": doc_code})
        return parse_parameters(response, doc_code)

    def export_pdf_raw(
        self, doc_code: str, payload: Sequence[Mapping[str, Any]]
    ) -> bytes:
        """``POST ExportPDFData?DocCode=…`` with a caller-built payload.

        The verbatim escape hatch: ``payload`` is sent as-is (it must already
        be the ``[{"name","type","value":[[…]]}, …]`` array). Prefer
        :meth:`export_pdf`, which builds it from ``LoadCR``.

        Returns:
            The decoded PDF bytes (magic bytes verified).

        Raises:
            APIGatewayParameterError: the gateway answered ``(---)`` twice.
            APIGatewayPDFError: the body decoded to something that is not a PDF.

        Concurrency: at most ``config.max_concurrent_exports`` exports run at
        once per client (semaphore), and a ``(---)`` answer is retried exactly
        once — the gateway drops some renders when several run in parallel on
        one session, and the export is idempotent.
        """
        body = list(payload)
        with self._export_slot():
            response = self._request(
                "POST", "ExportPDFData", params={"DocCode": doc_code}, json=body
            )
            try:
                return decode_pdf(response, doc_code)
            except APIGatewayParameterError:
                self._logger.warning(
                    "ExportPDFData for %r answered '(---)' - retrying once...",
                    doc_code,
                )
            response = self._request(
                "POST", "ExportPDFData", params={"DocCode": doc_code}, json=body
            )
            return decode_pdf(response, doc_code)

    def export_pdf(
        self,
        doc_code: str,
        values: Mapping[str, Any] | None = None,
        *,
        parameters: Sequence[ReportParameter] | None = None,
        strict: bool = True,
    ) -> bytes:
        """Render a layout to PDF.

        Fetches the parameter definitions (unless ``parameters`` is given),
        merges ``values`` following the gateway's rules (see
        :func:`b1sl.api_gateway.payload.build_export_payload`) and exports.

        Args:
            doc_code: Layout code (``RCRI0018``, ``QUT20020`` …).
            values: ``{param_name: value}`` — scalars, dates, or sequences
                (a date range is ``(start, end)``).
            parameters: Reuse a previous ``get_report_parameters()`` result
                to skip the ``LoadCR`` round-trip.
            strict: Reject unknown names / missing required values locally.
        """
        if parameters is None:
            parameters = self.get_report_parameters(doc_code)
        payload = build_export_payload(parameters, values, strict=strict)
        return self.export_pdf_raw(doc_code, payload)

    def export_document_pdf(
        self,
        doc_code: str,
        doc_entry: int | str,
        *,
        object_id: int | str | None = None,
        values: Mapping[str, Any] | None = None,
        parameters: Sequence[ReportParameter] | None = None,
    ) -> bytes:
        """Print one SAP document with a document-bound layout.

        Always sets ``DocKey@`` explicitly — the value ``LoadCR`` preloads
        travels with the layout definition and may point at an arbitrary
        document, so relying on it would silently print the wrong one.
        ``ObjectId@`` is taken from ``LoadCR`` unless ``object_id`` is given.

        Args:
            doc_code: Layout code from Print Layout Designer (``QUT20020``).
            doc_entry: ``DocEntry`` of the document to print.
            object_id: SAP object type (``23`` = Quotations …). Optional.
            values: Extra parameter values for the layout.
            parameters: Cached ``get_report_parameters()`` result.
        """
        if parameters is None:
            parameters = self.get_report_parameters(doc_code)
        merged = self._document_values(
            doc_code, doc_entry, object_id, values, parameters
        )
        return self.export_pdf(doc_code, merged, parameters=parameters)
