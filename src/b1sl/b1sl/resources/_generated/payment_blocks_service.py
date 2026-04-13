from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class PaymentBlocksService(GenericResource[Any]):
    endpoint = "PaymentBlocksService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_payment_block_list(self, payload: dict | None = None) -> Any:
        """POST PaymentBlocksService_GetPaymentBlockList
        Invoke the method 'GetPaymentBlockList' on this service.
        """
        return self._adapter.post(f"PaymentBlocksService_GetPaymentBlockList", data=payload)
