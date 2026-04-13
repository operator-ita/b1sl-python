from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ResourceCapacitiesService(GenericResource[Any]):
    endpoint = "ResourceCapacitiesService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_list(self, payload: dict | None = None) -> Any:
        """POST ResourceCapacitiesService_GetList
        Invoke the method 'GetList' on this service.
        """
        return self._adapter.post(f"ResourceCapacitiesService_GetList", data=payload)

    def get_list_with_filter(self, payload: dict | None = None) -> Any:
        """POST ResourceCapacitiesService_GetListWithFilter
        Invoke the method 'GetListWithFilter' on this service by specifying the payload 'ResourceCapacityWithFilterParams' in the JSON format.

        Example:
        ```json
        {
            "ResourceCapacityWithFilterParams": {}
        }
        ```
        """
        return self._adapter.post(f"ResourceCapacitiesService_GetListWithFilter", data=payload)
