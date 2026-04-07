from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class AlternativeItemsService(GenericResource[Any]):
    endpoint = "AlternativeItemsService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def add_item(self, payload: dict | None = None) -> Any:
        """POST AlternativeItemsService_AddItem
        Invoke the method 'AddItem' on this service by specifying the payload 'OriginalItem' in the JSON format.

        Example:
        ```json
        {
            "OriginalItem": {
                "AlternativeItems": [
                    {
                        "AlternativeItemCode": "B001",
                        "MatchFactor": 100,
                        "Remarks": "B001"
                    },
                    {
                        "AlternativeItemCode": "I002",
                        "MatchFactor": 100,
                        "Remarks": "I002"
                    },
                    {
                        "AlternativeItemCode": "I003",
                        "MatchFactor": 100,
                        "Remarks": "I003"
                    }
                ],
                "ItemCode": "I001",
                "ItemName": null
            }
        }
        ```
        """
        return self._adapter.post(f"AlternativeItemsService_AddItem", data=payload)

    def delete_item(self, payload: dict | None = None) -> Any:
        """POST AlternativeItemsService_DeleteItem
        Invoke the method 'DeleteItem' on this service by specifying the payload 'OriginalItemParams' in the JSON format.

        Example:
        ```json
        {
            "OriginalItem": {
                "ItemCode": "I001",
                "ItemName": "I001"
            }
        }
        ```
        """
        return self._adapter.post(f"AlternativeItemsService_DeleteItem", data=payload)

    def get_item(self, payload: dict | None = None) -> Any:
        """POST AlternativeItemsService_GetItem
        Invoke the method 'GetItem' on this service by specifying the payload 'OriginalItemParams' in the JSON format.

        Example:
        ```json
        {
            "OriginalItem": {
                "ItemCode": "I001",
                "ItemName": "I001"
            }
        }
        ```
        """
        return self._adapter.post(f"AlternativeItemsService_GetItem", data=payload)

    def update_item(self, payload: dict | None = None) -> Any:
        """POST AlternativeItemsService_UpdateItem
        Invoke the method 'UpdateItem' on this service by specifying the payload 'OriginalItem' in the JSON format.

        Example:
        ```json
        {
            "OriginalItem": {
                "AlternativeItems": [
                    {
                        "AlternativeItemCode": "B001",
                        "MatchFactor": 100,
                        "Remarks": "B001"
                    },
                    {
                        "AlternativeItemCode": "I002",
                        "MatchFactor": 100,
                        "Remarks": "I002"
                    },
                    {
                        "AlternativeItemCode": "I003",
                        "MatchFactor": 100,
                        "Remarks": "I003"
                    }
                ],
                "ItemCode": "I001",
                "ItemName": null
            }
        }
        ```
        """
        return self._adapter.post(f"AlternativeItemsService_UpdateItem", data=payload)
