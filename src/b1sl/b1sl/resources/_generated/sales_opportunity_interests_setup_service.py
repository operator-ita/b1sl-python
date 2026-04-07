from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class SalesOpportunityInterestsSetupService(GenericResource[Any]):
    endpoint = "SalesOpportunityInterestsSetupService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_sales_opportunity_interest_setup_list(self, payload: dict | None = None) -> Any:
        """POST SalesOpportunityInterestsSetupService_GetSalesOpportunityInterestSetupList
        Invoke the method 'GetSalesOpportunityInterestSetupList' on this service.
        """
        return self._adapter.post("SalesOpportunityInterestsSetupService_GetSalesOpportunityInterestSetupList", data=payload)
