from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CustomsGroupsService(GenericResource["CustomsGroup"]):
    """This entity enables you to manipulate 'CustomsGroups'. It defines custom groups, which specify the customs duty for items purchased abroad that are liable for customs."""
    endpoint = "CustomsGroups"
    
    def __init__(self, adapter):
        from ...models._generated._types import CustomsGroup
        self.model = CustomsGroup
        super().__init__(adapter)
