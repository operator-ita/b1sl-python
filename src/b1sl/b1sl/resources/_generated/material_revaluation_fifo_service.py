from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class MaterialRevaluationFIFOService(GenericResource[Any]):
    endpoint = "MaterialRevaluationFIFOService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_material_revaluation_fifo(self, payload: dict | None = None) -> Any:
        """POST MaterialRevaluationFIFOService_GetMaterialRevaluationFIFO
        Invoke the method 'GetMaterialRevaluationFIFO' on this service by specifying the payload 'MaterialRevaluationFIFOParams' in the JSON format.

        Example:
        ```json
        {
            "MaterialRevaluationFIFOParams": {
                "ItemCode": "I001",
                "LocationCode": null,
                "LocationType": null,
                "ShowIssuedLayers": "tNO"
            }
        }
        ```
        """
        return self._adapter.post(f"MaterialRevaluationFIFOService_GetMaterialRevaluationFIFO", data=payload)
