from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ServiceCallOriginsService(GenericResource[Any]):
    endpoint = "ServiceCallOriginsService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_service_call_origin_list(self, payload: dict | None = None) -> Any:
        """POST ServiceCallOriginsService_GetServiceCallOriginList
        Invoke the method 'GetServiceCallOriginList' on this service.
        """
        return self._adapter.post(f"ServiceCallOriginsService_GetServiceCallOriginList", data=payload)
