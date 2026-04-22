from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import BatchClient

class ChangeSetContext:
    """
    Manages the lifecycle of a ChangeSet in OData.
    Ensures that operations are atomic and prohibits GETs.
    """
    def __init__(self, batch_client: BatchClient):
        self._batch = batch_client
        self._changeset_id = f"changeset_{uuid.uuid4()}"

    def __enter__(self) -> BatchClient:
        self._batch.active_changeset_id = self._changeset_id
        return self._batch

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._batch.active_changeset_id = None

    async def __aenter__(self) -> BatchClient:
        return self.__enter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return self.__exit__(exc_type, exc_val, exc_tb)
