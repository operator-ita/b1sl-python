from __future__ import annotations

import copy
import functools
import inspect
import logging
import re
import uuid
from typing import TYPE_CHECKING, Any, Callable

import httpx

from ._recording_adapter import (
    PendingRequest,
    _RecordingAdapter,
    _SyncRecordingAdapter,
)
from .changeset import ChangeSetContext
from .parser import BatchParser
from .results import BatchResult, BatchResults
from .serializer import BatchSerializer

if TYPE_CHECKING:
    from b1sl.b1sl import AsyncB1Client, B1Client

logger = logging.getLogger("b1sl.BatchClient")

class ResourceProxy:
    """Recursive proxy for capturing batch requests."""
    def __init__(self, target: Any, adapter: _RecordingAdapter, client: BatchClient):
        self._target = target
        self._adapter = adapter
        self._client = client

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            return getattr(self._target, name)
        attr = getattr(self._target, name)
        if inspect.iscoroutinefunction(attr):
            return self._wrap_async(attr)
        if callable(attr):
            return self._wrap_callable(attr)
        return attr

    def _capture_model(self) -> None:
        """Point the recording adapter at the model behind the proxied target."""
        model = getattr(self._target, "model", None)
        if model is None and hasattr(self._target, "_resource"):
            model = getattr(self._target._resource, "model", None)
        self._adapter._current_model = model

    def _wrap_async(self, method: Callable) -> Callable:
        @functools.wraps(method)
        async def wrapper(*args, **kwargs):
            self._capture_model()
            try:
                await method(*args, **kwargs)
            except (AttributeError, TypeError) as e:
                # Post-processing of the recording adapter's fake Result can
                # fail (the request is already enqueued, so this is harmless),
                # but log it: a real infrastructure bug would otherwise hide here.
                logger.debug(
                    "Batch proxy suppressed %s in %s: %s",
                    type(e).__name__, getattr(method, "__qualname__", method), e,
                )
            return None
        return wrapper

    def _wrap_callable(self, method: Callable) -> Callable:
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            self._capture_model()
            try:
                result = method(*args, **kwargs)
            except (AttributeError, TypeError) as e:
                # Same suppression policy as _wrap_async.
                logger.debug(
                    "Batch proxy suppressed %s in %s: %s",
                    type(e).__name__, getattr(method, "__qualname__", method), e,
                )
                return None
            if hasattr(result, "_adapter") or hasattr(result, "_resource"):
                # Chaining object (resource / QueryBuilder): repoint it at the
                # recording adapter and keep proxying the fluent chain.
                if hasattr(result, "_adapter"):
                    setattr(result, "_adapter", self._adapter)
                if hasattr(result, "_resource") and hasattr(result._resource, "_adapter"):
                    setattr(result._resource, "_adapter", self._adapter)
                return ResourceProxy(result, self._adapter, self._client)
            return result
        return wrapper

class BatchClient:
    """OData Batch Orchestrator (asynchronous)."""
    def __init__(self, b1_session: AsyncB1Client | B1Client):
        self._b1 = b1_session
        self._pending: list[PendingRequest] = []
        self._adapter: _RecordingAdapter = _RecordingAdapter(self)
        self.active_changeset_id: str | None = None
        self._batch_boundary = f"batch_{uuid.uuid4()}"

    def __getattr__(self, name: str) -> Any:
        real_resource = getattr(self._b1, name)
        new_resource = copy.copy(real_resource)
        if hasattr(new_resource, "_adapter"):
            new_resource._adapter = self._adapter
        return ResourceProxy(new_resource, self._adapter, self)

    def changeset(self) -> ChangeSetContext:
        return ChangeSetContext(self)

    def _extract_response_boundary(self, response_content_type: str) -> str | None:
        """Extracts the boundary string from a SAP Content-Type response header."""
        match = re.search(r"boundary=([^\s;]+)", response_content_type)
        if match:
            return match.group(1).strip().replace('"', '')
        return None

    def _serialize_pending(self) -> tuple[str, dict]:
        """Serializes the recorded operations into a multipart body + headers."""
        serializer = BatchSerializer(self._pending, self._batch_boundary)
        body = serializer.serialize()
        headers = {"Content-Type": f"multipart/mixed; boundary={self._batch_boundary}"}
        return body, headers

    def _parse_response(self, response: httpx.Response) -> BatchResults:
        """Parses SAP's multipart response into BatchResults."""
        # IMPORTANT: Use the boundary that SAP returns in its response
        resp_ct = response.headers.get("Content-Type", "")
        resp_boundary = self._extract_response_boundary(resp_ct)

        # Fallback: use the request boundary if SAP omits it in the response
        boundary_to_use = resp_boundary or self._batch_boundary

        parser = BatchParser(response.text, boundary_to_use)
        expected_models = [req.model_type for req in self._pending]
        raw_results = parser.parse(expected_models)

        return BatchResults(raw_results)

    def _dry_run_results(self) -> BatchResults:
        """Synthesizes an all-204 result set without touching SAP (Dry Run)."""
        logger.info(
            "[DRY RUN] Intercepting $batch with %d operation(s) — nothing sent to SAP.",
            len(self._pending),
        )
        return BatchResults([
            BatchResult(status=204, data=None, model_type=req.model_type, index=i)
            for i, req in enumerate(self._pending)
        ])

    async def execute(self) -> BatchResults:
        """Dynamically serializes, sends, and parses the batch."""
        if not self._pending:
            return BatchResults([])

        real_adapter = getattr(self._b1, "_adapter")
        # Dry Run guards every write path, including $batch: simulate per-op
        # 204s instead of sending the multipart request.
        if getattr(real_adapter, "_dry_run_active", False):
            return self._dry_run_results()

        body, headers = self._serialize_pending()
        response = await real_adapter.post_batch(body, headers)
        return self._parse_response(response)

    async def __aenter__(self) -> BatchClient:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        # Reset internal state to prevent accidental reuse of a consumed BatchClient.
        self._pending.clear()
        self.active_changeset_id = None


class SyncBatchClient(BatchClient):
    """OData Batch Orchestrator for the synchronous B1Client."""

    def __init__(self, b1_session: B1Client):
        super().__init__(b1_session)
        self._adapter = _SyncRecordingAdapter(self)

    def execute(self) -> BatchResults:  # type: ignore[override]
        """Serializes, sends, and parses the batch synchronously."""
        if not self._pending:
            return BatchResults([])

        real_adapter = getattr(self._b1, "_adapter")
        if getattr(real_adapter, "_dry_run_active", False):
            return self._dry_run_results()

        body, headers = self._serialize_pending()
        response = real_adapter.post_batch(body, headers)
        return self._parse_response(response)

    def __enter__(self) -> SyncBatchClient:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._pending.clear()
        self.active_changeset_id = None
