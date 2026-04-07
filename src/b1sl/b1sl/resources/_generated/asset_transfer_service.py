from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class AssetTransferService(GenericResource[Any]):
    endpoint = "AssetTransferService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def cancel(self, payload: dict | None = None) -> Any:
        """POST AssetTransferService_Cancel
        Invoke the method 'Cancel' on this service by specifying the payload 'AssetDocumentParams' in the JSON format.

        Example:
        ```json
        {
            "AssetDocumentParams": {
                "CancellationOption": "coByOriginalDocumentDate",
                "Code": "2"
            }
        }
        ```
        """
        return self._adapter.post("AssetTransferService_Cancel", data=payload)

    def get_list(self, payload: dict | None = None) -> Any:
        """POST AssetTransferService_GetList
        Invoke the method 'GetList' on this service.
        """
        return self._adapter.post("AssetTransferService_GetList", data=payload)
