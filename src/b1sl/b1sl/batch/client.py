from __future__ import annotations

import copy
import functools
import inspect
import re
import uuid
from typing import TYPE_CHECKING, Any, Callable

from ._recording_adapter import PendingRequest, _RecordingAdapter
from .changeset import ChangeSetContext
from .parser import BatchParser
from .results import BatchResults
from .serializer import BatchSerializer

if TYPE_CHECKING:
    from b1sl.b1sl import AsyncB1Client, B1Client

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

    def _wrap_async(self, method: Callable) -> Callable:
        @functools.wraps(method)
        async def wrapper(*args, **kwargs):
            model = getattr(self._target, "model", None)
            if model is None and hasattr(self._target, "_resource"):
                model = getattr(self._target._resource, "model", None)
            self._adapter._current_model = model
            try:
                await method(*args, **kwargs)
            except (AttributeError, TypeError):
                # Suppress infrastructure errors from the proxy mechanism;
                # business-logic exceptions (e.g. ValueError for GET-in-ChangeSet)
                # are intentionally allowed to propagate.
                pass
            return None
        return wrapper

    def _wrap_callable(self, method: Callable) -> Callable:
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            result = method(*args, **kwargs)
            if hasattr(result, "__dict__") or hasattr(result, "_adapter"):
                if hasattr(result, "_adapter"):
                    setattr(result, "_adapter", self._adapter)
                if hasattr(result, "_resource") and hasattr(result._resource, "_adapter"):
                    setattr(result._resource, "_adapter", self._adapter)
                return ResourceProxy(result, self._adapter, self._client)
            return result
        return wrapper

class BatchClient:
    """OData Batch Orchestrator."""
    def __init__(self, b1_session: AsyncB1Client | B1Client):
        self._b1 = b1_session
        self._pending: list[PendingRequest] = []
        self._adapter = _RecordingAdapter(self)
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

    async def execute(self) -> BatchResults:
        """Dynamically serializes, sends, and parses the batch."""
        if not self._pending:
            return BatchResults([])

        serializer = BatchSerializer(self._pending, self._batch_boundary)
        body = serializer.serialize()

        real_adapter = getattr(self._b1, "_adapter") 
        headers = {"Content-Type": f"multipart/mixed; boundary={self._batch_boundary}"}
        
        response = await real_adapter.post_batch(body, headers)
        
        # IMPORTANT: Use the boundary that SAP returns in its response
        resp_ct = response.headers.get("Content-Type", "")
        resp_boundary = self._extract_response_boundary(resp_ct)

        # Fallback: use the request boundary if SAP omits it in the response
        boundary_to_use = resp_boundary or self._batch_boundary

        parser = BatchParser(response.text, boundary_to_use)
        expected_models = [req.model_type for req in self._pending]
        raw_results = parser.parse(expected_models)
        
        return BatchResults(raw_results)

    async def __aenter__(self) -> BatchClient:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        # Reset internal state to prevent accidental reuse of a consumed BatchClient.
        self._pending.clear()
        self.active_changeset_id = None
