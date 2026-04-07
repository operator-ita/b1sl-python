from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class NFTaxCategoriesService(GenericResource[Any]):
    endpoint = "NFTaxCategoriesService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_list(self, payload: dict | None = None) -> Any:
        """POST NFTaxCategoriesService_GetList
        Invoke the method 'GetList' on this service.
        """
        return self._adapter.post("NFTaxCategoriesService_GetList", data=payload)
