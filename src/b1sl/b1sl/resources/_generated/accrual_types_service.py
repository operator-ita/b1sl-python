from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class AccrualTypesService(GenericResource[Any]):
    endpoint = "AccrualTypesService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_accrual_type_list(self, payload: dict | None = None) -> Any:
        """POST AccrualTypesService_GetAccrualTypeList
        Invoke the method 'GetAccrualTypeList' on this service.
        """
        return self._adapter.post(f"AccrualTypesService_GetAccrualTypeList", data=payload)
