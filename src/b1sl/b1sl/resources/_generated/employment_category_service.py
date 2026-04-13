from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class EmploymentCategoryService(GenericResource[Any]):
    endpoint = "EmploymentCategoryService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_employment_category_list(self, payload: dict | None = None) -> Any:
        """POST EmploymentCategoryService_GetEmploymentCategoryList
        Invoke the method 'GetEmploymentCategoryList' on this service.
        """
        return self._adapter.post(f"EmploymentCategoryService_GetEmploymentCategoryList", data=payload)
