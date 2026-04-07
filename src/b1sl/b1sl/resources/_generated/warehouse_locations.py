from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class WarehouseLocationsService(GenericResource["WarehouseLocation"]):
    """This entity enables you to manipulate 'WarehouseLocations'. It defines the geographical locations of the warehouses."""
    endpoint = "WarehouseLocations"

    def __init__(self, adapter):
        from ...models._generated._types import WarehouseLocation
        self.model = WarehouseLocation
        super().__init__(adapter)
