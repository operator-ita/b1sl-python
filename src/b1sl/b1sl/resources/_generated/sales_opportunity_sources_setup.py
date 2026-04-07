from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class SalesOpportunitySourcesSetupService(GenericResource["SalesOpportunitySourceSetup"]):
    """This entity enables you to manipulate 'SalesOpportunitySourcesSetup'."""
    endpoint = "SalesOpportunitySourcesSetup"
    
    def __init__(self, adapter):
        from ...models._generated._types import SalesOpportunitySourceSetup
        self.model = SalesOpportunitySourceSetup
        super().__init__(adapter)
