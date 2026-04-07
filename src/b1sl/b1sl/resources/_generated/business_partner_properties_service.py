from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class BusinessPartnerPropertiesService(GenericResource[Any]):
    endpoint = "BusinessPartnerPropertiesService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_business_partner_property_list(self, payload: dict | None = None) -> Any:
        """POST BusinessPartnerPropertiesService_GetBusinessPartnerPropertyList
        Invoke the method 'GetBusinessPartnerPropertyList' on this service.
        """
        return self._adapter.post(f"BusinessPartnerPropertiesService_GetBusinessPartnerPropertyList", data=payload)
