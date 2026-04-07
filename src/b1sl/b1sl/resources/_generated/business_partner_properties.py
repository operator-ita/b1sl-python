from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class BusinessPartnerPropertiesService(GenericResource["BusinessPartnerProperty"]):
    """This entity enables you to manipulate 'BusinessPartnerProperties'."""
    endpoint = "BusinessPartnerProperties"

    def __init__(self, adapter):
        from ...models._generated._types import BusinessPartnerProperty
        self.model = BusinessPartnerProperty
        super().__init__(adapter)
