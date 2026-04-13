from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class PredefinedTextsService(GenericResource[Any]):
    endpoint = "PredefinedTextsService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_predefined_text_list(self, payload: dict | None = None) -> Any:
        """POST PredefinedTextsService_GetPredefinedTextList
        Invoke the method 'GetPredefinedTextList' on this service.
        """
        return self._adapter.post(f"PredefinedTextsService_GetPredefinedTextList", data=payload)
