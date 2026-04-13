from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class PickListsService(GenericResource["PickList"]):
    """This entity enables you to manipulate 'PickLists'. It supports the picking process of items from the warehouse. The picking process applies only to items that are already approved in sales orders."""
    endpoint = "PickLists"
    
    def __init__(self, adapter):
        from ...models._generated._types import PickList
        self.model = PickList
        super().__init__(adapter)
