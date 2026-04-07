from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ResourcePropertiesService(GenericResource[Any]):
    endpoint = "ResourcePropertiesService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_list(self, payload: dict | None = None) -> Any:
        """POST ResourcePropertiesService_GetList
        Invoke the method 'GetList' on this service.
        """
        return self._adapter.post("ResourcePropertiesService_GetList", data=payload)
