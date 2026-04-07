from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class PaymentReasonCodeService(GenericResource[Any]):
    endpoint = "PaymentReasonCodeService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_payment_reason_code_list(self, payload: dict | None = None) -> Any:
        """POST PaymentReasonCodeService_GetPaymentReasonCodeList
        Invoke the method 'GetPaymentReasonCodeList' on this service.
        """
        return self._adapter.post(f"PaymentReasonCodeService_GetPaymentReasonCodeList", data=payload)
