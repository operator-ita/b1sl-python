from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CostElementService(GenericResource[Any]):
    endpoint = "CostElementService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_cost_element_list(self, payload: dict | None = None) -> Any:
        """POST CostElementService_GetCostElementList
        Invoke the method 'GetCostElementList' on this service.
        """
        return self._adapter.post("CostElementService_GetCostElementList", data=payload)
