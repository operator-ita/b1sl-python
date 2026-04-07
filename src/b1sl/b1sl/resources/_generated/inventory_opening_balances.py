from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class InventoryOpeningBalancesService(GenericResource["InventoryOpeningBalance"]):
    """This entity enables you to manipulate 'InventoryOpeningBalances'."""
    endpoint = "InventoryOpeningBalances"

    def __init__(self, adapter):
        from ...models._generated._types import InventoryOpeningBalance
        self.model = InventoryOpeningBalance
        super().__init__(adapter)
