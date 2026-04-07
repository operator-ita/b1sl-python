from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class InventoryPostingsService(GenericResource[Any]):
    endpoint = "InventoryPostingsService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_list(self, payload: dict | None = None) -> Any:
        """POST InventoryPostingsService_GetList
        Invoke the method 'GetList' on this service.
        """
        return self._adapter.post(f"InventoryPostingsService_GetList", data=payload)

    def set_copy_option(self, payload: dict | None = None) -> Any:
        """POST InventoryPostingsService_SetCopyOption
        Invoke the method 'SetCopyOption' on this service by specifying the payload 'InventoryPostingCopyOption' in the JSON format.

        Example:
        ```json
        {
            "InventoryPostingCopyOption": {}
        }
        ```
        """
        return self._adapter.post(f"InventoryPostingsService_SetCopyOption", data=payload)
