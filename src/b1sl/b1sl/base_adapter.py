from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from b1sl.b1sl.config import B1Config
import asyncio
import json
import logging
import uuid
from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from urllib.parse import parse_qs, urlencode, urlparse

from b1sl.b1sl.exceptions.exceptions import SAPConcurrencyError


@dataclass
class ObservabilityConfig:
    """
    Configuration for SDK observability features.

    Attributes:
        hooks (dict): Dictionary mapping event names to lists of callables.
            Supported events: 'on_response', 'on_error'.
        context_extras (dict): Arbitrary metadata injected into every HookContext.
        slow_request_threshold_ms (float): Threshold to trigger 'slow request' logs.
        log_level_slow (int): Logging level for slow requests. Default is logging.WARNING.
    """

    hooks: Dict[str, List[Callable]] = field(default_factory=dict)
    context_extras: Dict[str, Any] = field(default_factory=dict)
    slow_request_threshold_ms: float = 5000.0
    log_level_slow: int = logging.WARNING


@dataclass(frozen=True, slots=True)
class HookContext:
    """
    Immutable object passed to every hook on response or error.
    Designed for structured logging and performance monitoring.

    Privacy Note: URL components are separated to avoid logging sensitive
    data contained in query parameters by default.
    """

    req_id: str
    http_method: str
    base_url: str
    endpoint: str
    query_params: str  # Raw query string
    db: str
    user: str
    status_code: Optional[int]  # None if network exception occurred
    duration_ms: float
    payload: Optional[Dict[str, Any]] = None  # Redacted request body
    if_match: Optional[str] = None  # ETag sent in If-Match
    extra: Dict[str, Any] = field(default_factory=dict)
    exc: Optional[Exception] = None

    @property
    def duration_s(self) -> float:
        """Duration in seconds."""
        return self.duration_ms / 1000.0

    def to_log_extra(self) -> Dict[str, Any]:
        """Generate a flat dictionary for structured loggers."""
        return {
            "req_id": self.req_id,
            "http_method": self.http_method,
            "base_url": self.base_url,
            "endpoint": self.endpoint,
            "db": self.db,
            "user": self.user,
            "status_code": self.status_code,
            "duration_ms": round(self.duration_ms, 3),
            "payload": self.payload,
            "if_match": self.if_match,
            **self.extra,
        }


class HookDispatcher:
    """
    Safely manages and executes event hooks.

    Hook Contract for authors:
    - ctx is immutable; any modification attempt will raise FrozenInstanceError.
    - Hooks are executed in order of registration (sequential).
    - An exception in a hook DOES NOT interrupt subsequent hooks or the SDK request.
    - Errors in hooks are caught and logged at WARNING level via exc_info.
    - duration_ms is always available, even on network errors (status_code=None).
    """

    def __init__(self, hooks: Dict[str, List[Callable]] | None = None):
        self._hooks = hooks or {}

    def dispatch(self, event: str, ctx: HookContext, logger: logging.Logger) -> None:
        """Synchronously dispatch a hook event."""
        for hook in self._hooks.get(event, []):
            try:
                hook(ctx)
            except Exception as e:
                name = getattr(hook, "__name__", "unnamed_hook")
                logger.warning(
                    f"Hook '{event}' (sync) {name} failed: {e}", exc_info=True
                )

    async def adispatch(
        self, event: str, ctx: HookContext, logger: logging.Logger
    ) -> None:
        """Asynchronously dispatch a hook event (supports both sync and async hooks concurrently)."""
        async def run_hook(hook: Callable) -> None:
            try:
                result = hook(ctx)
                if asyncio.iscoroutine(result):
                    await result
            except Exception as e:
                name = getattr(hook, "__name__", "unnamed_hook")
                logger.warning(
                    f"Hook '{event}' (async) {name} failed: {e}", exc_info=True
                )

        hooks = self._hooks.get(event, [])
        if hooks:
            await asyncio.gather(*(run_hook(h) for h in hooks))


class BaseRestAdapter:
    """
    Base class for SAP B1 Service Layer HTTP adapters.

    Provides shared logic for URL normalization, ETag caching,
    and structured observability (logging + hooks).
    """

    def __init__(
        self,
        config: B1Config,
        *,
        logger: logging.Logger | None = None,
        version: str = "v2",
        observability: ObservabilityConfig | None = None,
    ):
        self._config = config
        self.version = version
        base_url_stripped = config.base_url.rstrip("/")

        # URL Normalization logic
        if "/b1s/" not in base_url_stripped:
            self.raw_base_url = f"{base_url_stripped}/b1s/{version}"
        else:
            self.raw_base_url = base_url_stripped

        # Extract attributes from config for quick access or legacy internal use
        self._username = config.username
        self._password = config.password
        self._db = config.company_db
        self._ssl_verify = config.ssl_verify

        self.reuse_token = config.reuse_token
        self.token_timeout = config.token_timeout
        self.token_expiry: datetime | None = None
        self.is_session_active = False

        self._connect_timeout = config.connect_timeout
        self._read_timeout = config.read_timeout

        self._logger = logger or logging.getLogger(f"b1sl.{self.__class__.__name__}")

        # Observability Setup
        self._obs = observability or ObservabilityConfig()
        self._hooks = HookDispatcher(self._obs.hooks)

        self._etag_cache: OrderedDict[str, str] = OrderedDict()
        self._etag_max_size: int = getattr(config, "etag_cache_size", 256)

        # ContextVar: each asyncio task / thread gets its own dry_run value.
        # The ContextVar is per-instance to allow different clients to have
        # different global defaults independently.
        self._dry_run_var: ContextVar[bool] = ContextVar(
            f"dry_run_{id(self)}", default=config.dry_run
        )

    @property
    def _dry_run_active(self) -> bool:
        """Returns the current effective dry_run state for this task/thread."""
        return self._dry_run_var.get()

    @contextmanager
    def dry_run(self, enabled: bool = True):
        """
        Context manager to temporarily enable or disable Dry Run mode
        **for the current asyncio task / thread only**.

        Uses ``contextvars.ContextVar`` so that concurrent tasks sharing the
        same adapter instance do NOT interfere with each other.

        Usage::

            # Intercept writes in this block even if global dry_run is False
            with client.dry_run():
                await client.items.create(new_item)  # intercepted

            # Force real execution even if global dry_run is True
            with client.dry_run(enabled=False):
                await client.items.update(item)  # sent to SAP

        Note:
            Use ``with``, not ``async with`` — the context manager is
            synchronous even in async code, which is correct and idiomatic.
        """
        token = self._dry_run_var.set(enabled)
        try:
            yield
        finally:
            self._dry_run_var.reset(token)

    @classmethod
    def from_config(
        cls,
        config: B1Config,
        *,
        logger: logging.Logger | None = None,
        version: str = "v2",
        observability: ObservabilityConfig | None = None,
    ):
        """
        Factory method to instantiate the adapter from a B1Config.
        """
        return cls(
            config=config,
            logger=logger,
            version=version,
            observability=observability,
        )

    @property
    def url(self) -> str:
        """Returns the fully normalized Service Layer base URL (including /b1s/v1)."""
        return self.raw_base_url

    def _clear_etag(self, key: str) -> None:
        """Remove an ETag from the cache (e.g. after a conflict)."""
        if key in self._etag_cache:
            del self._etag_cache[key]

    def _set_etag(self, key: str, value: str) -> None:
        """Update the ETag for a given resource in the LRU cache.

        The key is always the canonical endpoint path (e.g.
        ``/BusinessPartners('C20000')``) so that both GET and subsequent
        PATCH/DELETE operations share the same lookup key.
        """
        if key in self._etag_cache:
            self._etag_cache.move_to_end(key)
        self._etag_cache[key] = value
        if len(self._etag_cache) > self._etag_max_size:
            self._etag_cache.popitem(last=False)

    def _extract_etag(
        self,
        endpoint: str,
        response_headers: dict,
        response_body: dict | None,
    ) -> str | None:
        """Extract and cache the ETag for a resource after a successful request.

        Extraction priority (per SAP B1 OData V4 spec):
        1. ``ETag`` response header  (preferred — avoids altering body parsing)
        2. ``@odata.etag`` key inside the JSON body  (fallback for SAP quirks)

        The extracted value is automatically stored in the LRU cache.

        Args:
            endpoint: The canonical resource path used as the cache key.
            response_headers: Mapping of HTTP response headers.
            response_body: Parsed JSON body, or ``None`` when the response has
                no content (e.g. 204 No Content).

        Returns:
            The raw ETag string (including surrounding quotes and ``W/`` prefix)
            or ``None`` when no ETag was found.
        """
        etag = response_headers.get("ETag") or response_headers.get("etag")
        if not etag and isinstance(response_body, dict):
            etag = response_body.get("@odata.etag")
        if etag:
            self._set_etag(endpoint, etag)
        return etag or None

    def _build_headers(
        self,
        http_method: str,
        endpoint: str,
        extra_headers: dict | None = None,
    ) -> dict:
        """Build the final HTTP headers for a request, injecting ETag controls.

        Injection rules:
        - ``GET``: Adds ``If-None-Match`` if an ETag is cached (enables 304
          Not Modified optimisation — note SAP SL may not honour this).
        - ``PATCH`` / ``DELETE`` / ``POST`` (actions): Adds ``If-Match`` with
          the cached ETag when one is available, enforcing optimistic concurrency.
          If no ETag is cached the header is **omitted**, which causes SAP to
          perform a blind override (documented SAP behaviour).

        Args:
            http_method: HTTP verb in upper-case.
            endpoint: Canonical resource path, used to look up the ETag cache.
            extra_headers: Optional caller-supplied headers that take precedence
                over the defaults built here.

        Returns:
            A new ``dict`` ready to pass to the underlying HTTP library.
        """
        headers: dict = {"Content-Type": "application/json"}

        cached_etag = self._etag_cache.get(endpoint)

        if http_method == "GET" and cached_etag:
            headers["If-None-Match"] = cached_etag
        elif http_method in {"PATCH", "DELETE", "POST"} and cached_etag:
            # POST covers OData Actions (e.g. /BusinessPartners('C20000')/Cancel)
            headers["If-Match"] = cached_etag

        if extra_headers:
            headers.update(extra_headers)
        return headers

    def _raise_if_concurrency_error(
        self,
        status_code: int,
        sap_code: str,
        sap_message: str,
        endpoint: str,
        response_body: dict | None,
    ) -> None:
        """Convert a SAP 412 + code -2039 response into a ``SAPConcurrencyError``.

        This is the *single* place where the SDK distinguishes an ETag conflict
        from a generic HTTP error.  Both sync and async adapters call this
        method right before raising their generic ``B1Exception``, so the
        specialised exception is always raised first when applicable.

        Args:
            status_code: HTTP status code of the failed response.
            sap_code: SAP OData error code extracted from the response body.
            sap_message: Human-readable SAP error message.
            endpoint: Resource path where the conflict occurred.
            response_body: Full parsed JSON body for the ``details`` attribute.

        Raises:
            SAPConcurrencyError: Always, when status_code is 412 and
                sap_code is ``"-2039"``.
        """
        if status_code == 412 and sap_code == SAPConcurrencyError.SAP_ERROR_CODE:
            etag_sent = self._etag_cache.get(endpoint)
            self._clear_etag(endpoint)  # Force fresh GET on next attempt
            raise SAPConcurrencyError(
                f"ETag conflict on '{endpoint}': {sap_message}",
                sap_code=sap_code,
                etag_sent=etag_sent,
                endpoint=endpoint,
                details=response_body,
            )

    def _redact_data(self, data: dict | None) -> dict:
        """Mask sensitive information in data dictionaries before logging."""
        return {k: "***" if k == "Password" else v for k, v in (data or {}).items()}

    def _generate_req_id(self) -> str:
        """Generate a short unique identifier for request tracing."""
        return uuid.uuid4().hex[:16]

    def _log_response(self, ctx: HookContext) -> None:
        """
        Standardized logging for request outcomes.
        Elevates level if duration exceeds threshold.
        """
        level = logging.INFO
        status_label = f" -> {ctx.status_code}" if ctx.status_code else " -> ERROR"
        slow_label = ""

        if ctx.duration_ms >= self._obs.slow_request_threshold_ms:
            level = self._obs.log_level_slow
            slow_label = " ⚠ SLOW"

        if ctx.exc:
            level = logging.ERROR

        clean_endpoint = ctx.endpoint.lstrip("/")
        msg = f"[{ctx.req_id}][{ctx.user}] [{ctx.http_method} /{clean_endpoint}]{status_label} ({ctx.duration_ms:.1f}ms){slow_label}"
        
        # In Dry Run or Debug mode, we might want to see the body in the main message
        meta_info = []
        if ctx.if_match:
            meta_info.append(f"ETag: {ctx.if_match}")
            
        if ctx.extra.get("is_dry_run") and ctx.payload:
            payload_str = json.dumps(ctx.payload)
            meta_info.append(f"Body: {payload_str}")
            
        if meta_info:
            msg += f" | {' | '.join(meta_info)}"
            
        self._logger.log(level, msg, extra=ctx.to_log_extra())

    # ── URL Helpers ──────────────────────────────────────────────────────── #

    def _clean_url(self, next_link: str) -> str:
        """Normalize an OData nextLink by sorting query parameters."""
        parsed_url = urlparse(next_link)
        query_params = parse_qs(parsed_url.query)
        cleaned_query = urlencode(query_params, doseq=True)
        return parsed_url._replace(query=cleaned_query).geturl()

    def _get_ep_params(self, next_link: str) -> dict:
        """Extract query parameters from an OData nextLink into a dictionary."""
        parsed_url = urlparse(next_link)
        query_params = parse_qs(parsed_url.query)
        return {k: ",".join(v) for k, v in query_params.items()}

    # ── SAP OData error parsing ──────────────────────────────────────────── #

    @staticmethod
    def _parse_sap_error_shared(
        status_code: int, reason: str, body: Any
    ) -> tuple[str, str]:
        """Extract SAP-specific error code and message from an OData response."""
        http_fallback = f"HTTP {status_code}: {reason}"
        if not isinstance(body, dict):
            return "unknown", http_fallback

        error_node = body.get("error")
        if not error_node:
            return "unknown", http_fallback

        if isinstance(error_node, str):
            return "unknown", error_node

        if not isinstance(error_node, dict):
            return "unknown", http_fallback

        sap_code = str(error_node.get("code", "unknown"))
        raw_message = error_node.get("message", "")

        if isinstance(raw_message, dict):
            sap_message = raw_message.get("value") or raw_message.get(
                "lang", http_fallback
            )
        elif isinstance(raw_message, str) and raw_message:
            sap_message = raw_message
        else:
            sap_message = http_fallback

        return sap_code, sap_message

