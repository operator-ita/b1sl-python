from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class BusinessPartnerGroupsService(GenericResource["BusinessPartnerGroup"]):
    """This entity enables you to manipulate 'BusinessPartnerGroups'. It represents the setup of customer and vendor groups. Used for classifying business partners according to different criteria, such as sector or size."""
    endpoint = "BusinessPartnerGroups"
    
    def __init__(self, adapter):
        from ...models._generated._types import BusinessPartnerGroup
        self.model = BusinessPartnerGroup
        super().__init__(adapter)
