from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class AccountCategoryService(GenericResource[Any]):
    endpoint = "AccountCategoryService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_category_list(self, payload: dict | None = None) -> Any:
        """POST AccountCategoryService_GetCategoryList
        Invoke the method 'GetCategoryList' on this service.
        """
        return self._adapter.post("AccountCategoryService_GetCategoryList", data=payload)
