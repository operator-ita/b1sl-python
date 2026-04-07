from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class BankChargesAllocationCodesService(GenericResource[Any]):
    endpoint = "BankChargesAllocationCodesService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_bank_charges_allocation_code_list(self, payload: dict | None = None) -> Any:
        """POST BankChargesAllocationCodesService_GetBankChargesAllocationCodeList
        Invoke the method 'GetBankChargesAllocationCodeList' on this service.
        """
        return self._adapter.post("BankChargesAllocationCodesService_GetBankChargesAllocationCodeList", data=payload)
