from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class InventoryTransferRequestsService(GenericResource["StockTransfer"]):
    """This entity enables you to manipulate 'InventoryTransferRequests'. It represents a request to transfer inventory from one warehouse to another. After the requested quantity is received by the receiving warehouse, you can close the inventory transfer request and create an inventory transfer document."""
    endpoint = "InventoryTransferRequests"
    
    def __init__(self, adapter):
        from ...models._generated._types import StockTransfer
        self.model = StockTransfer
        super().__init__(adapter)
