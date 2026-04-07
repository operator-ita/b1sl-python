from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class SalesOpportunitySourcesSetupService(GenericResource[Any]):
    endpoint = "SalesOpportunitySourcesSetupService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_sales_opportunity_source_setup_list(self, payload: dict | None = None) -> Any:
        """POST SalesOpportunitySourcesSetupService_GetSalesOpportunitySourceSetupList
        Invoke the method 'GetSalesOpportunitySourceSetupList' on this service.
        """
        return self._adapter.post("SalesOpportunitySourcesSetupService_GetSalesOpportunitySourceSetupList", data=payload)
