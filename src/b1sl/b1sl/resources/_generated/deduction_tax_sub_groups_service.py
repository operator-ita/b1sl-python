from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class DeductionTaxSubGroupsService(GenericResource[Any]):
    endpoint = "DeductionTaxSubGroupsService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_deduction_tax_sub_group_list(self, payload: dict | None = None) -> Any:
        """POST DeductionTaxSubGroupsService_GetDeductionTaxSubGroupList
        Invoke the method 'GetDeductionTaxSubGroupList' on this service.
        """
        return self._adapter.post(f"DeductionTaxSubGroupsService_GetDeductionTaxSubGroupList", data=payload)
