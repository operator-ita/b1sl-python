from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class BusinessPlacesService(GenericResource["BusinessPlace"]):
    """This entity enables you to manipulate 'BusinessPlaces'. It represents a company's business locations."""
    endpoint = "BusinessPlaces"
    
    def __init__(self, adapter):
        from ...models._generated._types import BusinessPlace
        self.model = BusinessPlace
        super().__init__(adapter)
