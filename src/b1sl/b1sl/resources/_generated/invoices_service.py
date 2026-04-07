from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class InvoicesService(GenericResource[Any]):
    endpoint = "InvoicesService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def approve_and_add(self, payload: dict | None = None) -> Any:
        """POST InvoicesService_ApproveAndAdd
        """
        return self._adapter.post("InvoicesService_ApproveAndAdd", data=payload)

    def approve_and_update(self, payload: dict | None = None) -> Any:
        """POST InvoicesService_ApproveAndUpdate
        """
        return self._adapter.post("InvoicesService_ApproveAndUpdate", data=payload)

    def cancel2(self, payload: dict | None = None) -> Any:
        """POST InvoicesService_Cancel2
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
        return self._adapter.post("InvoicesService_Cancel2", data=payload)

    def close_by_date(self, payload: dict | None = None) -> Any:
        """POST InvoicesService_CloseByDate
        """
        return self._adapter.post("InvoicesService_CloseByDate", data=payload)

    def export_e_way_bill(self, payload: dict | None = None) -> Any:
        """POST InvoicesService_ExportEWayBill
        """
        return self._adapter.post("InvoicesService_ExportEWayBill", data=payload)

    def get_approval_templates(self, payload: dict | None = None) -> Any:
        """POST InvoicesService_GetApprovalTemplates
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
                        "UnitPrice": "30"
                    }
                ]
            }
        }
        ```
        """
        return self._adapter.post("InvoicesService_GetApprovalTemplates", data=payload)

    def handle_approval_request(self, payload: dict | None = None) -> Any:
        """POST InvoicesService_HandleApprovalRequest
        Invoke the method 'HandleApprovalRequest' on this service.
        """
        return self._adapter.post("InvoicesService_HandleApprovalRequest", data=payload)

    def init_data(self, payload: dict | None = None) -> Any:
        """POST InvoicesService_InitData
        """
        return self._adapter.post("InvoicesService_InitData", data=payload)

    def request_approve_cancellation(self, payload: dict | None = None) -> Any:
        """POST InvoicesService_RequestApproveCancellation
        Invoke the method 'RequestApproveCancellation' on this service by specifying the payload 'Document' in the JSON format.

        Example:
        ```json
        {
            "Document": {
                "DocEntry": "123"
            }
        }
        ```
        """
        return self._adapter.post("InvoicesService_RequestApproveCancellation", data=payload)
