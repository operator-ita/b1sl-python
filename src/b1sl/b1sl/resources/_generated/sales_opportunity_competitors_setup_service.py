from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class SalesOpportunityCompetitorsSetupService(GenericResource[Any]):
    endpoint = "SalesOpportunityCompetitorsSetupService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_sales_opportunity_competitor_setup_list(self, payload: dict | None = None) -> Any:
        """POST SalesOpportunityCompetitorsSetupService_GetSalesOpportunityCompetitorSetupList
        Invoke the method 'GetSalesOpportunityCompetitorSetupList' on this service.
        """
        return self._adapter.post(f"SalesOpportunityCompetitorsSetupService_GetSalesOpportunityCompetitorSetupList", data=payload)
