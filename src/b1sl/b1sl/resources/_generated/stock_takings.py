from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class StockTakingsService(GenericResource["StockTaking"]):
    """This entity enables you to manipulate 'StockTakings'."""
    endpoint = "StockTakings"
    
    def __init__(self, adapter):
        from ...models._generated._types import StockTaking
        self.model = StockTaking
        super().__init__(adapter)
