from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class AssetCapitalizationCreditMemoService(GenericResource[Any]):
    endpoint = "AssetCapitalizationCreditMemoService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def cancel(self, payload: dict | None = None) -> Any:
        """POST AssetCapitalizationCreditMemoService_Cancel
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
        return self._adapter.post(f"AssetCapitalizationCreditMemoService_Cancel", data=payload)

    def get_list(self, payload: dict | None = None) -> Any:
        """POST AssetCapitalizationCreditMemoService_GetList
        Invoke the method 'GetList' on this service.
        """
        return self._adapter.post(f"AssetCapitalizationCreditMemoService_GetList", data=payload)
