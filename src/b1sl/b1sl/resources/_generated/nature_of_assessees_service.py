from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class NatureOfAssesseesService(GenericResource[Any]):
    endpoint = "NatureOfAssesseesService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_nature_of_assessee_list(self, payload: dict | None = None) -> Any:
        """POST NatureOfAssesseesService_GetNatureOfAssesseeList
        Invoke the method 'GetNatureOfAssesseeList' on this service.
        """
        return self._adapter.post(f"NatureOfAssesseesService_GetNatureOfAssesseeList", data=payload)
