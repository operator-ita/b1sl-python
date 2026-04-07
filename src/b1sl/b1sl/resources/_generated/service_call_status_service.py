from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ServiceCallStatusService(GenericResource[Any]):
    endpoint = "ServiceCallStatusService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_service_call_status_list(self, payload: dict | None = None) -> Any:
        """POST ServiceCallStatusService_GetServiceCallStatusList
        Invoke the method 'GetServiceCallStatusList' on this service.
        """
        return self._adapter.post(f"ServiceCallStatusService_GetServiceCallStatusList", data=payload)
