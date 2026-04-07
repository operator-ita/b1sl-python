from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class InventoryGenEntryService(GenericResource[Any]):
    endpoint = "InventoryGenEntryService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def approve_and_add(self, payload: dict | None = None) -> Any:
        """POST InventoryGenEntryService_ApproveAndAdd
        """
        return self._adapter.post("InventoryGenEntryService_ApproveAndAdd", data=payload)

    def approve_and_update(self, payload: dict | None = None) -> Any:
        """POST InventoryGenEntryService_ApproveAndUpdate
        """
        return self._adapter.post("InventoryGenEntryService_ApproveAndUpdate", data=payload)

    def close_by_date(self, payload: dict | None = None) -> Any:
        """POST InventoryGenEntryService_CloseByDate
        """
        return self._adapter.post("InventoryGenEntryService_CloseByDate", data=payload)

    def export_e_way_bill(self, payload: dict | None = None) -> Any:
        """POST InventoryGenEntryService_ExportEWayBill
        """
        return self._adapter.post("InventoryGenEntryService_ExportEWayBill", data=payload)

    def get_approval_templates(self, payload: dict | None = None) -> Any:
        """POST InventoryGenEntryService_GetApprovalTemplates
        Invoke the method 'GetApprovalTemplates' on this service by specifying the payload 'Document' in the JSON format.

        Example:
        ```json
        {
            "Document": {
                "DocumentLines": [
                    {
                        "ItemCode": "i001",
                        "Quantity": "100",
                        "UnitPrice": "1"
                    }
                ]
            }
        }
        ```
        """
        return self._adapter.post("InventoryGenEntryService_GetApprovalTemplates", data=payload)

    def handle_approval_request(self, payload: dict | None = None) -> Any:
        """POST InventoryGenEntryService_HandleApprovalRequest
        Invoke the method 'HandleApprovalRequest' on this service.
        """
        return self._adapter.post("InventoryGenEntryService_HandleApprovalRequest", data=payload)

    def init_data(self, payload: dict | None = None) -> Any:
        """POST InventoryGenEntryService_InitData
        """
        return self._adapter.post("InventoryGenEntryService_InitData", data=payload)
