from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ItemPropertiesService(GenericResource["ItemProperty"]):
    """This entity enables you to manipulate 'ItemProperties'."""
    endpoint = "ItemProperties"
    
    def __init__(self, adapter):
        from ...models._generated._types import ItemProperty
        self.model = ItemProperty
        super().__init__(adapter)
