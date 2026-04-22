from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Type

from b1sl.b1sl.models.result import Result

if TYPE_CHECKING:
    from b1sl.b1sl.models.base import B1Model

    from .client import BatchClient

@dataclass
class PendingRequest:
    """Represents an enqueued request within a batch."""
    method: str
    endpoint: str
    data: dict | None = None
    ep_params: dict | None = None
    model_type: Type[B1Model] | None = None
    changeset_id: str | None = None
    content_id: str = field(default_factory=lambda: str(uuid.uuid4()))

class _RecordingAdapter:
    """
    Internal adapter that captures requests instead of executing them.
    Complies with the RestAdapterProtocol asynchronously.
    """
    def __init__(self, batch_client: BatchClient):
        self._batch = batch_client
        self._current_model: Type[B1Model] | None = None

    def _record(self, method: str, endpoint: str, ep_params: dict | None = None, data: dict | None = None):
        """Captures the request and adds it to the client's queue."""
        if method == "GET" and self._batch.active_changeset_id:
            raise ValueError("OData Batch Error: GET operations are not allowed within a ChangeSet.")

        req = PendingRequest(
            method=method,
            endpoint=endpoint,
            ep_params=ep_params,
            data=data,
            model_type=self._current_model,
            changeset_id=self._batch.active_changeset_id
        )
        self._batch._pending.append(req)
        
        # Return a simulated Result so Pydantic doesn't crash
        return Result(status_code=202, data={})

    # Asynchronous implementation for AsyncGenericResource
    async def get(self, endpoint, ep_params=None, data=None):
        return self._record("GET", endpoint, ep_params, data)

    async def post(self, endpoint, ep_params=None, data=None):
        return self._record("POST", endpoint, ep_params, data)

    async def patch(self, endpoint, ep_params=None, data=None):
        return self._record("PATCH", endpoint, ep_params, data)

    async def delete(self, endpoint, ep_params=None, data=None):
        return self._record("DELETE", endpoint, ep_params, data)

    # Synchronous implementation for GenericResource (compatibility)
    def get_sync(self, endpoint, ep_params=None, data=None):
        return self._record("GET", endpoint, ep_params, data)
