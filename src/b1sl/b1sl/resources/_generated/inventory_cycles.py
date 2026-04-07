from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class InventoryCyclesService(GenericResource["InventoryCycles"]):
    """This entity enables you to manipulate 'InventoryCycles'. It allows to set up cycles of inventory counts and order intervals."""
    endpoint = "InventoryCycles"

    def __init__(self, adapter):
        from ...models._generated._types import InventoryCycles
        self.model = InventoryCycles
        super().__init__(adapter)
