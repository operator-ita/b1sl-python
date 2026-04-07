from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class PurchaseInvoicesService(GenericResource[Any]):
    endpoint = "PurchaseInvoicesService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def approve_and_add(self, payload: dict | None = None) -> Any:
        """POST PurchaseInvoicesService_ApproveAndAdd
        """
        return self._adapter.post(f"PurchaseInvoicesService_ApproveAndAdd", data=payload)

    def approve_and_update(self, payload: dict | None = None) -> Any:
        """POST PurchaseInvoicesService_ApproveAndUpdate
        """
        return self._adapter.post(f"PurchaseInvoicesService_ApproveAndUpdate", data=payload)

    def cancel2(self, payload: dict | None = None) -> Any:
        """POST PurchaseInvoicesService_Cancel2
        Invoke the method 'Cancel2' on this service by specifying the payload 'Document' in the JSON format. This method allows you to change some properties before cancelling one document.

        Example:
        ```json
        {
            "Document": {
                "Comments": "via SL.",
                "DocEntry": 123
            }
        }
        ```
        """
        return self._adapter.post(f"PurchaseInvoicesService_Cancel2", data=payload)

    def close_by_date(self, payload: dict | None = None) -> Any:
        """POST PurchaseInvoicesService_CloseByDate
        """
        return self._adapter.post(f"PurchaseInvoicesService_CloseByDate", data=payload)

    def export_e_way_bill(self, payload: dict | None = None) -> Any:
        """POST PurchaseInvoicesService_ExportEWayBill
        """
        return self._adapter.post(f"PurchaseInvoicesService_ExportEWayBill", data=payload)

    def get_approval_templates(self, payload: dict | None = None) -> Any:
        """POST PurchaseInvoicesService_GetApprovalTemplates
        Invoke the method 'GetApprovalTemplates' on this service by specifying the payload 'Document' in the JSON format.

        Example:
        ```json
        {
            "Document": {
                "CardCode": "c001",
                "DocumentLines": [
                    {
                        "ItemCode": "i001",
                        "Quantity": "100",
                        "TaxCode": "T1",
                        "UnitPrice": "50"
                    }
                ]
            }
        }
        ```
        """
        return self._adapter.post(f"PurchaseInvoicesService_GetApprovalTemplates", data=payload)

    def handle_approval_request(self, payload: dict | None = None) -> Any:
        """POST PurchaseInvoicesService_HandleApprovalRequest
        Invoke the method 'HandleApprovalRequest' on this service.
        """
        return self._adapter.post(f"PurchaseInvoicesService_HandleApprovalRequest", data=payload)

    def init_data(self, payload: dict | None = None) -> Any:
        """POST PurchaseInvoicesService_InitData
        """
        return self._adapter.post(f"PurchaseInvoicesService_InitData", data=payload)
