from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class FixedAssetItemsService(GenericResource[Any]):
    endpoint = "FixedAssetItemsService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_asset_end_balance(self, payload: dict | None = None) -> Any:
        """POST FixedAssetItemsService_GetAssetEndBalance
        Invoke the method 'GetAssetEndBalance' on this service by specifying the payload 'FixedAssetValuesParams' in the JSON format.

        Example:
        ```json
        {
            "FixedAssetValuesParams": {}
        }
        ```
        """
        return self._adapter.post(f"FixedAssetItemsService_GetAssetEndBalance", data=payload)

    def get_asset_values_list(self, payload: dict | None = None) -> Any:
        """POST FixedAssetItemsService_GetAssetValuesList
        Invoke the method 'GetAssetValuesList' on this service by specifying the payload 'FixedAssetValuesParams' in the JSON format.

        Example:
        ```json
        {
            "FixedAssetValuesParams": {}
        }
        ```
        """
        return self._adapter.post(f"FixedAssetItemsService_GetAssetValuesList", data=payload)

    def update_asset_end_balance(self, payload: dict | None = None) -> Any:
        """POST FixedAssetItemsService_UpdateAssetEndBalance
        Invoke the method 'UpdateAssetEndBalance' on this service by specifying the payload 'FixedAssetValuesParams,FixedAssetEndBalance' in the JSON format.

        Example:
        ```json
        {
            "FixedAssetEndBalance": {},
            "FixedAssetValuesParams": {}
        }
        ```
        """
        return self._adapter.post(f"FixedAssetItemsService_UpdateAssetEndBalance", data=payload)
