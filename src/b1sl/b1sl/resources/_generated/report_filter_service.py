from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ReportFilterService(GenericResource[Any]):
    endpoint = "ReportFilterService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_tax_report_filter_list(self, payload: dict | None = None) -> Any:
        """POST ReportFilterService_GetTaxReportFilterList
        Invoke the method 'GetTaxReportFilterList' on this service by specifying the payload 'TaxReportFilterParams' in the JSON format.

        Example:
        ```json
        {
            "TaxReportFilterParams": {
                "Code": 1
            }
        }
        ```
        """
        return self._adapter.post(f"ReportFilterService_GetTaxReportFilterList", data=payload)
