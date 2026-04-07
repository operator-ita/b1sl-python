from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class SalesOpportunityReasonsSetupService(GenericResource[Any]):
    endpoint = "SalesOpportunityReasonsSetupService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_sales_opportunity_reason_setup_list(self, payload: dict | None = None) -> Any:
        """POST SalesOpportunityReasonsSetupService_GetSalesOpportunityReasonSetupList
        Invoke the method 'GetSalesOpportunityReasonSetupList' on this service.
        """
        return self._adapter.post("SalesOpportunityReasonsSetupService_GetSalesOpportunityReasonSetupList", data=payload)
