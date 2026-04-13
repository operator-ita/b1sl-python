from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CashDiscountsService(GenericResource[Any]):
    endpoint = "CashDiscountsService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_cash_discount_list(self, payload: dict | None = None) -> Any:
        """POST CashDiscountsService_GetCashDiscountList
        Invoke the method 'GetCashDiscountList' on this service.
        """
        return self._adapter.post(f"CashDiscountsService_GetCashDiscountList", data=payload)
