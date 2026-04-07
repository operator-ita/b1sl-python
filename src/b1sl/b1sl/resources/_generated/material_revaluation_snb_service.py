from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class MaterialRevaluationSNBService(GenericResource[Any]):
    endpoint = "MaterialRevaluationSNBService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def add(self, payload: dict | None = None) -> Any:
        """POST MaterialRevaluationSNBService_Add
        """
        return self._adapter.post("MaterialRevaluationSNBService_Add", data=payload)

    def get_list(self, payload: dict | None = None) -> Any:
        """POST MaterialRevaluationSNBService_GetList
        Invoke the method 'GetList' on this service by specifying the payload 'MaterialRevaluationSNBParam' in the JSON format.

        Example:
        ```json
        {
            "MaterialRevaluationSNBParam": {}
        }
        ```
        """
        return self._adapter.post("MaterialRevaluationSNBService_GetList", data=payload)
