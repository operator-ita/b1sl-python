from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ReportTypesService(GenericResource[Any]):
    endpoint = "ReportTypesService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_report_type_list(self, payload: dict | None = None) -> Any:
        """POST ReportTypesService_GetReportTypeList
        Invoke the method 'GetReportTypeList' on this service.
        """
        return self._adapter.post("ReportTypesService_GetReportTypeList", data=payload)
