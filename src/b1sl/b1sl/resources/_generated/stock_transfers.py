from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class StockTransfersService(GenericResource["StockTransfer"]):
    """This entity enables you to manipulate 'StockTransfers'. It represents transfer records of items from one warehouse to another."""
    endpoint = "StockTransfers"

    def __init__(self, adapter):
        from ...models._generated._types import StockTransfer
        self.model = StockTransfer
        super().__init__(adapter)
