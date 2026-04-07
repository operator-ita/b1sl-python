from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CashFlowLineItemsService(GenericResource[Any]):
    endpoint = "CashFlowLineItemsService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_cash_flow_line_item_list(self, payload: dict | None = None) -> Any:
        """POST CashFlowLineItemsService_GetCashFlowLineItemList
        Invoke the method 'GetCashFlowLineItemList' on this service.
        """
        return self._adapter.post("CashFlowLineItemsService_GetCashFlowLineItemList", data=payload)
