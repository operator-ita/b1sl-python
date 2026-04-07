from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class DepartmentsService(GenericResource[Any]):
    endpoint = "DepartmentsService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_department_list(self, payload: dict | None = None) -> Any:
        """POST DepartmentsService_GetDepartmentList
        Invoke the method 'GetDepartmentList' on this service.
        """
        return self._adapter.post("DepartmentsService_GetDepartmentList", data=payload)
