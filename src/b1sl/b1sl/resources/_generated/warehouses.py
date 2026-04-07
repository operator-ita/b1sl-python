from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class WarehousesService(GenericResource["Warehouse"]):
    """This entity enables you to manipulate 'Warehouses'. It represents the information of warehouses in the Inventory module."""
    endpoint = "Warehouses"
    
    def __init__(self, adapter):
        from ...models._generated._types import Warehouse
        self.model = Warehouse
        super().__init__(adapter)
