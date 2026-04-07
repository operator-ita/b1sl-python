from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class PriceListsService(GenericResource["PriceList"]):
    """This entity enables you to manipulate 'PriceLists'. It represents the management of price lists in the Inventory module. An item can have several prices, with each based on a different price list, for example, purchase price list, sales price list, distributor price list, and so on."""
    endpoint = "PriceLists"

    def __init__(self, adapter):
        from ...models._generated._types import PriceList
        self.model = PriceList
        super().__init__(adapter)
