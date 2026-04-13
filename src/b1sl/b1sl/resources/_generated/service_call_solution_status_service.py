from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ServiceCallSolutionStatusService(GenericResource[Any]):
    endpoint = "ServiceCallSolutionStatusService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_service_call_solution_status_list(self, payload: dict | None = None) -> Any:
        """POST ServiceCallSolutionStatusService_GetServiceCallSolutionStatusList
        Invoke the method 'GetServiceCallSolutionStatusList' on this service.
        """
        return self._adapter.post(f"ServiceCallSolutionStatusService_GetServiceCallSolutionStatusList", data=payload)
