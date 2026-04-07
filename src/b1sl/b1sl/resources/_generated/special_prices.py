from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class SpecialPricesService(GenericResource["SpecialPrice"]):
    """This entity enables you to manipulate 'SpecialPrices'. It represents a discount for a specific item in a specific price list. The discount can apply to a specific business partner or for all business partners. For a specific business partner, the item and business partner must be unique; for all business partners, the item and price list must be unique."""
    endpoint = "SpecialPrices"
    
    def __init__(self, adapter):
        from ...models._generated._types import SpecialPrice
        self.model = SpecialPrice
        super().__init__(adapter)
