from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ServiceGroupsService(GenericResource[Any]):
    endpoint = "ServiceGroupsService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_service_group_list(self, payload: dict | None = None) -> Any:
        """POST ServiceGroupsService_GetServiceGroupList
        Invoke the method 'GetServiceGroupList' on this service.
        """
        return self._adapter.post(f"ServiceGroupsService_GetServiceGroupList", data=payload)
