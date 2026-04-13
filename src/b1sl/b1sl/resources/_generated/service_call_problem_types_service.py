from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ServiceCallProblemTypesService(GenericResource[Any]):
    endpoint = "ServiceCallProblemTypesService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_service_call_problem_type_list(self, payload: dict | None = None) -> Any:
        """POST ServiceCallProblemTypesService_GetServiceCallProblemTypeList
        Invoke the method 'GetServiceCallProblemTypeList' on this service.
        """
        return self._adapter.post(f"ServiceCallProblemTypesService_GetServiceCallProblemTypeList", data=payload)
