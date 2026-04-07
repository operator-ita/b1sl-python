from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class MaterialGroupsService(GenericResource[Any]):
    endpoint = "MaterialGroupsService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_material_group_list(self, payload: dict | None = None) -> Any:
        """POST MaterialGroupsService_GetMaterialGroupList
        Invoke the method 'GetMaterialGroupList' on this service.
        """
        return self._adapter.post(f"MaterialGroupsService_GetMaterialGroupList", data=payload)
