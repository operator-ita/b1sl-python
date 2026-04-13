from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class StatesService(GenericResource[Any]):
    endpoint = "StatesService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_state_list(self, payload: dict | None = None) -> Any:
        """POST StatesService_GetStateList
        Invoke the method 'GetStateList' on this service.
        """
        return self._adapter.post(f"StatesService_GetStateList", data=payload)
