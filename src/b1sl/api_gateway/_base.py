"""
b1sl.api_gateway._base
~~~~~~~~~~~~~~~~~~~~~~
Transport-agnostic core shared by ``APIGatewayClient`` (sync) and
``AsyncAPIGatewayClient``: configuration, session-expiry maths, hook/log
context, and the response decoders that turn the gateway's status-less
error signalling into typed exceptions.

The two twins differ only in the HTTP call itself (``httpx.Client`` vs
``httpx.AsyncClient``) and the lock primitive; everything that can be wrong
about *interpreting* the gateway lives here, once.
"""

from __future__ import annotations

import base64
import binascii
import logging
import time
import uuid
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any

import httpx

from b1sl.api_gateway.config import APIGatewayConfig
from b1sl.api_gateway.exceptions import (
    APIGatewayLayoutNotFoundError,
    APIGatewayParameterError,
    APIGatewayPDFError,
    APIGatewayResponseError,
)
from b1sl.api_gateway.models import ReportInfo, ReportParameter
from b1sl.b1sl.base_adapter import HookContext, HookDispatcher, ObservabilityConfig

REST_PREFIX = "/rs/v1"
LOGIN_PATH = "/login"
LOGOUT_PATH = "/logout"

#: ``ExportPDFData`` answers ``200 OK`` with this literal body when the
#: parameter payload is malformed. No HTTP error is raised by the gateway.
MALFORMED_PAYLOAD_SENTINEL = b"(---)"
PDF_MAGIC = b"%PDF-"

#: Parameter names every document-bound layout (``QUT200xx`` …) exposes.
DOC_KEY_PARAM = "DocKey@"
OBJECT_ID_PARAM = "ObjectId@"

#: Statuses that mean "no valid session" and trigger one re-login + retry.
#: ``401`` (empty body) is the verified answer to a missing/invalid cookie;
#: ``403`` and redirects are covered defensively. Every endpoint is a read,
#: so the retry is idempotent.
SESSION_LOST_STATUSES = frozenset({401, 403})


def is_session_lost(status_code: int) -> bool:
    return status_code in SESSION_LOST_STATUSES or 300 <= status_code < 400


class BaseAPIGatewayClient:
    """State and pure logic shared by the sync and async clients."""

    def __init__(
        self,
        config: APIGatewayConfig,
        *,
        logger: logging.Logger | None = None,
        observability: ObservabilityConfig | None = None,
    ) -> None:
        self._config = config
        self.base_url = config.base_url
        self._logger = logger or logging.getLogger("b1sl.api_gateway")
        self._obs = observability or ObservabilityConfig()
        self._hooks = HookDispatcher(self._obs.hooks)

        self.is_session_active: bool = False
        self.token_expiry: datetime | None = None
        #: ``SessionTimeout`` as reported by the last successful ``/login``.
        self.server_session_timeout: int | float | None = None

        if not config.ssl_verify:
            self._logger.warning(
                "TLS certificate verification is DISABLED for the API Gateway "
                "(ssl_verify=False). Credentials and session cookies are exposed "
                "to man-in-the-middle attacks."
            )

    # ── Config-derived helpers ───────────────────────────────────────────── #

    def _login_payload(self) -> dict[str, str]:
        return {
            "CompanyDB": self._config.company_db,
            "UserName": self._config.username,
            "Password": self._config.password,
        }

    def _httpx_timeout(self) -> httpx.Timeout:
        cfg = self._config
        return httpx.Timeout(
            cfg.connect_timeout,
            read=cfg.read_timeout,
            write=cfg.read_timeout,
            pool=cfg.connect_timeout,
        )

    def _endpoint(self, path: str) -> str:
        return REST_PREFIX + (path if path.startswith("/") else f"/{path}")

    def _should_login(self) -> bool:
        if not self.is_session_active:
            return True
        if self.token_expiry is None:
            return False
        return datetime.now() >= self.token_expiry

    def _record_login(self, body: Any) -> dict[str, Any]:
        body = body if isinstance(body, dict) else {}
        self.server_session_timeout = body.get("SessionTimeout")
        self.token_expiry = self._compute_expiry(self.server_session_timeout)
        self.is_session_active = True
        return body

    def _compute_expiry(self, session_timeout: Any) -> datetime | None:
        """When to proactively re-login, or ``None`` for reactive-only.

        ``/login`` reports ``SessionTimeout: 30``, but a session measured
        live stayed valid after 32 min of pure idle and 40 min since login —
        the unit is not minutes and the real lifetime is unknown. Guessing
        would only create needless logins (and orphaned server sessions), so
        by default expiry is handled **reactively**: a ``401`` triggers one
        re-login + retry (verified behaviour). Set
        ``APIGatewayConfig.session_ttl`` to schedule proactive refreshes.
        """
        ttl = self._config.session_ttl
        if ttl is None:
            return None
        margin = min(self._config.session_refresh_margin, ttl / 4)
        return datetime.now() + ttl - margin

    def _forget_session(self) -> None:
        self.is_session_active = False
        self.token_expiry = None

    # ── Observability ────────────────────────────────────────────────────── #

    def _make_ctx(
        self,
        req_id: str,
        method: str,
        endpoint: str,
        query: str,
        response: httpx.Response | None,
        started: float,
        exc: Exception | None,
        payload: Any,
    ) -> HookContext:
        duration_ms = (time.perf_counter() - started) * 1000
        return HookContext(
            req_id=req_id,
            http_method=method,
            base_url=self.base_url,
            endpoint=endpoint,
            query_params=query,
            db=self._config.company_db,
            user=self._config.username,
            status_code=response.status_code if response is not None else None,
            duration_ms=duration_ms,
            payload=payload if isinstance(payload, dict) else None,
            extra={**self._obs.context_extras, "service": "api_gateway"},
            exc=exc,
        )

    def _log_ctx(self, ctx: HookContext) -> None:
        level = logging.ERROR if ctx.exc else logging.INFO
        slow = ""
        if ctx.duration_ms >= self._obs.slow_request_threshold_ms:
            if not ctx.exc:
                level = self._obs.log_level_slow
            slow = " ⚠ SLOW"
        status_label = (
            f" -> {ctx.status_code}" if ctx.status_code is not None else " -> ERROR"
        )
        self._logger.log(
            level,
            f"[{ctx.req_id}][{ctx.user}] [{ctx.http_method} {ctx.endpoint}]"
            f"{status_label} ({ctx.duration_ms:.1f}ms){slow}",
            extra=ctx.to_log_extra(),
        )

    # ── Request builders (shared by both twins) ──────────────────────────── #

    def _document_values(
        self,
        doc_code: str,
        doc_entry: int | str,
        object_id: int | str | None,
        values: Mapping[str, Any] | None,
        parameters: Sequence[ReportParameter],
    ) -> dict[str, Any]:
        """Merge ``doc_entry`` / ``object_id`` into ``values`` for a layout.

        Parameter names are resolved case-insensitively against what the
        layout declares (real layouts use both ``ObjectId@`` and
        ``ObjectID@``). ``object_id`` is dropped, with a debug log, when the
        layout has no object-type parameter at all — several document layouts
        take only ``DocKey@``.
        """
        by_lower = {p.name.lower(): p.name for p in parameters}
        doc_key_name = by_lower.get(DOC_KEY_PARAM.lower())
        if doc_key_name is None:
            raise APIGatewayParameterError(
                f"Layout {doc_code!r} has no {DOC_KEY_PARAM!r} parameter — it is "
                "not a document-bound layout. Use export_pdf() instead."
            )
        merged: dict[str, Any] = dict(values or {})
        merged[doc_key_name] = doc_entry
        if object_id is not None:
            object_name = by_lower.get(OBJECT_ID_PARAM.lower())
            if object_name is None:
                self._logger.debug(
                    "Layout %r declares no ObjectId@ parameter; ignoring object_id=%r",
                    doc_code,
                    object_id,
                )
            else:
                merged[object_name] = object_id
        return merged


# ── Response decoders ─────────────────────────────────────────────────────── #


def req_id() -> str:
    return uuid.uuid4().hex[:16]


def snippet(response: httpx.Response, limit: int = 200) -> str:
    text = response.text.strip()
    return text[:limit] + ("…" if len(text) > limit else "")


def body_details(response: httpx.Response) -> dict | None:
    try:
        body = response.json()
    except ValueError:
        return {"body": snippet(response, 500)} if response.content else None
    return body if isinstance(body, dict) else {"body": body}


def json_or_raise(response: httpx.Response, endpoint: str) -> dict[str, Any]:
    if not response.content:
        return {}
    try:
        body = response.json()
    except ValueError as e:
        raise APIGatewayResponseError(
            f"API Gateway {endpoint} returned a non-JSON body: {snippet(response)}",
            details={"body": snippet(response, 500)},
        ) from e
    if not isinstance(body, dict):
        raise APIGatewayResponseError(
            f"API Gateway {endpoint} returned an unexpected JSON shape: "
            f"{type(body).__name__}",
            details={"body": body},
        )
    return body


def error_envelope(body: Any) -> str | None:
    """Return the message of a gateway error envelope, or ``None``.

    The gateway reports application-level failures inside a 2xx as
    ``{"code": -1, "message": {"lang": "en-us", "value": "…"}}`` (bad
    credentials on ``/login``) or ``{"code": 400, "message": "400 BAD_REQUEST"}``.
    A successful body never carries ``code``.
    """
    if not isinstance(body, Mapping) or "code" not in body:
        return None
    code = body.get("code")
    if code in (0, "0", None):
        return None
    message = body.get("message")
    if isinstance(message, Mapping):
        message = message.get("value") or message.get("lang") or str(message)
    return f"[{code}] {message or 'unknown error'}"


def raise_if_failed(
    body: Mapping[str, Any], endpoint: str, response: httpx.Response
) -> None:
    envelope = error_envelope(body)
    if envelope:
        raise APIGatewayResponseError(
            f"API Gateway {endpoint} reported an error: {envelope}",
            details=dict(body),
        )
    if body.get("error") is True:  # LoadCR uses {"error": false, "resultSet": …}
        raise APIGatewayResponseError(
            f"API Gateway {endpoint} reported error=true: "
            f"{body.get('message') or snippet(response)}",
            details=dict(body),
        )
    result = body.get("result")
    if result is not None and str(result).lower() != "success":
        raise APIGatewayResponseError(
            f"API Gateway {endpoint} reported result={result!r}: "
            f"{body.get('message') or body.get('error') or snippet(response)}",
            details=dict(body),
        )


def parse_report_list(response: httpx.Response) -> list[ReportInfo]:
    body = json_or_raise(response, "LoadAuthorizedCRList")
    raise_if_failed(body, "LoadAuthorizedCRList", response)
    rows = body.get("resultSet") or []
    return [ReportInfo.from_wire(r) for r in rows if isinstance(r, Mapping)]


def parse_parameters(response: httpx.Response, doc_code: str) -> list[ReportParameter]:
    body = json_or_raise(response, "LoadCR")
    if not body or "resultSet" not in body:
        raise APIGatewayLayoutNotFoundError(doc_code, details=body or None)
    raise_if_failed(body, "LoadCR", response)
    rows = body.get("resultSet") or []
    return [ReportParameter.from_wire(r) for r in rows if isinstance(r, Mapping)]


def decode_pdf(response: httpx.Response, doc_code: str) -> bytes:
    """Turn an ``ExportPDFData`` 2xx body into verified PDF bytes.

    Success is decided by the *body*, never by ``200`` vs ``201``: the
    gateway flips between the two non-deterministically under concurrent
    calls while returning byte-identical PDFs.
    """
    content = response.content
    if content.startswith(PDF_MAGIC):
        return bytes(content)  # already binary — never strip a real PDF
    raw = content.strip()
    if raw == MALFORMED_PAYLOAD_SENTINEL:
        # ``(---)`` is the gateway's generic "could not render": malformed
        # payload, unknown DocCode, *or* a transient failure under concurrent
        # exports (observed 1/5 and 3/5 in rounds of five). The clients
        # retry once before letting this surface.
        raise APIGatewayParameterError(
            f"API Gateway declined to render {doc_code!r} (answered '(---)'): "
            "a parameter is malformed, an empty optional parameter was "
            "included, a value could not be parsed, the DocCode does not "
            "exist, or the export collided with concurrent exports (already "
            "retried once).",
            details={"body": raw.decode("ascii", "replace")},
        )
    if not raw:
        raise APIGatewayPDFError(
            f"API Gateway returned an empty body for ExportPDFData {doc_code!r}."
        )
    # Tolerate a JSON-quoted base64 string.
    if len(raw) >= 2 and raw[:1] == b'"' and raw[-1:] == b'"':
        raw = raw[1:-1]
    try:
        pdf = base64.b64decode(raw, validate=False)
    except (binascii.Error, ValueError) as e:
        raise APIGatewayPDFError(
            f"ExportPDFData body for {doc_code!r} is not base64: {snippet(response)}",
            details={"body": snippet(response, 500)},
        ) from e
    if not pdf.startswith(PDF_MAGIC):
        raise APIGatewayPDFError(
            f"ExportPDFData body for {doc_code!r} decoded to something that is "
            f"not a PDF (starts with {pdf[:8]!r})."
        )
    return pdf
