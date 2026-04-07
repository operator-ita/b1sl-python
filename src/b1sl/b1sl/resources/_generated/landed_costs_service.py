from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class LandedCostsService(GenericResource[Any]):
    endpoint = "LandedCostsService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_landed_cost_list(self, payload: dict | None = None) -> Any:
        """POST LandedCostsService_GetLandedCostList
        Invoke the method 'GetLandedCostList' on this service.
        """
        return self._adapter.post("LandedCostsService_GetLandedCostList", data=payload)
