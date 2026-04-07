from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ShortLinkMappingsService(GenericResource[Any]):
    endpoint = "ShortLinkMappingsService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def batch_delete(self, payload: dict | None = None) -> Any:
        """POST ShortLinkMappingsService_BatchDelete
        Invoke the method 'BatchDelete' on this service.
        """
        return self._adapter.post("ShortLinkMappingsService_BatchDelete", data=payload)

    def get_list(self, payload: dict | None = None) -> Any:
        """POST ShortLinkMappingsService_GetList
        """
        return self._adapter.post("ShortLinkMappingsService_GetList", data=payload)
