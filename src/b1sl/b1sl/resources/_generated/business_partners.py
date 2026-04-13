from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class BusinessPartnersService(GenericResource["BusinessPartner"]):
    """This entity enables you to manipulate 'BusinessPartners'. It represents the business partners master data in the Business Partners module. You can use this data to record and retrieve business partner (customers, vendors, and leads) information and schedule business partner activities."""
    endpoint = "BusinessPartners"
    
    def __init__(self, adapter):
        from ...models._generated._types import BusinessPartner
        self.model = BusinessPartner
        super().__init__(adapter)
