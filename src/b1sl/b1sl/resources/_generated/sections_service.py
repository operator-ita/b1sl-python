from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class SectionsService(GenericResource[Any]):
    endpoint = "SectionsService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_section_list(self, payload: dict | None = None) -> Any:
        """POST SectionsService_GetSectionList
        Invoke the method 'GetSectionList' on this service.
        """
        return self._adapter.post(f"SectionsService_GetSectionList", data=payload)
