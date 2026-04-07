from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class AssetCapitalizationService(GenericResource[Any]):
    endpoint = "AssetCapitalizationService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def cancel(self, payload: dict | None = None) -> Any:
        """POST AssetCapitalizationService_Cancel
        Invoke the method 'Cancel' on this service by specifying the payload 'AssetDocumentParams' in the JSON format.

        Example:
        ```json
        {
            "AssetDocumentParams": {
                "CancellationOption": "coByCurrentSystemDate",
                "Code": "1"
            }
        }
        ```
        """
        return self._adapter.post(f"AssetCapitalizationService_Cancel", data=payload)

    def get_list(self, payload: dict | None = None) -> Any:
        """POST AssetCapitalizationService_GetList
        Invoke the method 'GetList' on this service.
        """
        return self._adapter.post(f"AssetCapitalizationService_GetList", data=payload)
