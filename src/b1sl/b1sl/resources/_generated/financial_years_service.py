from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class FinancialYearsService(GenericResource[Any]):
    endpoint = "FinancialYearsService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_financial_year_list(self, payload: dict | None = None) -> Any:
        """POST FinancialYearsService_GetFinancialYearList
        Invoke the method 'GetFinancialYearList' on this service.
        """
        return self._adapter.post("FinancialYearsService_GetFinancialYearList", data=payload)
