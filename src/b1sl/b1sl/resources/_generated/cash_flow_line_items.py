from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CashFlowLineItemsService(GenericResource["CashFlowLineItem"]):
    """This entity enables you to manipulate 'CashFlowLineItems'."""
    endpoint = "CashFlowLineItems"
    
    def __init__(self, adapter):
        from ...models._generated._types import CashFlowLineItem
        self.model = CashFlowLineItem
        super().__init__(adapter)
