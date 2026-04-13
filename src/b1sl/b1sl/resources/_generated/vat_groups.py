from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class VatGroupsService(GenericResource["VatGroup"]):
    """This entity enables you to manipulate 'VatGroups'. It defines tax groups that can be assigned to business partners and items in sales and purchase documents."""
    endpoint = "VatGroups"
    
    def __init__(self, adapter):
        from ...models._generated._types import VatGroup
        self.model = VatGroup
        super().__init__(adapter)
