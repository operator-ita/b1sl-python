from __future__ import annotations

from collections.abc import Sequence
from contextlib import AbstractContextManager
from datetime import datetime
from typing import Any, Protocol

from b1sl.b1sl.models.multipart import MultipartFile
from b1sl.b1sl.models.result import Result


class RestAdapterProtocol(Protocol):
    """
    Interface protocol for components that execute HTTP requests
    against SAP B1 Service Layer and return Result objects.

    Implemented statically by both the real RestAdapter and its Fakes.
    Declares the full surface that B1Client and the resource layer rely on —
    keeping it complete lets mypy catch drift between the protocol, the real
    adapter, and the test fakes.
    """

    # ── Session state ─────────────────────────────────────────────────────────

    is_session_active: bool
    token_expiry: datetime | None
    reuse_token: bool

    @property
    def session_id(self) -> str | None: ...

    @property
    def url(self) -> str: ...

    # ── HTTP verbs ────────────────────────────────────────────────────────────

    def get(
        self, endpoint: str, ep_params: dict | None = None, data: dict | None = None, headers: dict | None = None
    ) -> Result: ...

    def post(
        self, endpoint: str, ep_params: dict | None = None, data: dict | None = None, headers: dict | None = None
    ) -> Result: ...

    def patch(
        self, endpoint: str, ep_params: dict | None = None, data: dict | None = None, headers: dict | None = None
    ) -> Result: ...

    def delete(
        self, endpoint: str, ep_params: dict | None = None, data: dict | None = None, headers: dict | None = None
    ) -> Result: ...

    def post_batch(self, body: str, headers: dict, _retry_once: bool = True) -> Any: ...

    # ── Raw transport (non-JSON bodies) ───────────────────────────────────────

    def post_multipart(
        self,
        endpoint: str,
        files: Sequence[MultipartFile],
        headers: dict | None = None,
        _retry_once: bool = True,
    ) -> Result: ...

    def get_binary(
        self,
        endpoint: str,
        ep_params: dict | None = None,
        headers: dict | None = None,
        _retry_once: bool = True,
    ) -> bytes: ...

    # ── Lifecycle & per-context modes ────────────────────────────────────────

    def close(self) -> None: ...

    def dry_run(self, enabled: bool = True) -> AbstractContextManager[None]: ...

    def with_schema(self, schema: str | None) -> AbstractContextManager[None]: ...
