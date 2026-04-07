from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CreditNotesService(GenericResource[Any]):
    endpoint = "CreditNotesService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def approve_and_add(self, payload: dict | None = None) -> Any:
        """POST CreditNotesService_ApproveAndAdd
        """
        return self._adapter.post("CreditNotesService_ApproveAndAdd", data=payload)

    def approve_and_update(self, payload: dict | None = None) -> Any:
        """POST CreditNotesService_ApproveAndUpdate
        """
        return self._adapter.post("CreditNotesService_ApproveAndUpdate", data=payload)

    def cancel2(self, payload: dict | None = None) -> Any:
        """POST CreditNotesService_Cancel2
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
        return self._adapter.post("CreditNotesService_Cancel2", data=payload)

    def close_by_date(self, payload: dict | None = None) -> Any:
        """POST CreditNotesService_CloseByDate
        """
        return self._adapter.post("CreditNotesService_CloseByDate", data=payload)

    def export_e_way_bill(self, payload: dict | None = None) -> Any:
        """POST CreditNotesService_ExportEWayBill
        """
        return self._adapter.post("CreditNotesService_ExportEWayBill", data=payload)

    def get_approval_templates(self, payload: dict | None = None) -> Any:
        """POST CreditNotesService_GetApprovalTemplates
        Invoke the method 'GetApprovalTemplates' on this service by specifying the payload 'Document' in the JSON format.

        Example:
        ```json
        {
            "Document": {
                "CardCode": "c001",
                "DocumentLines": [
                    {
                        "ItemCode": "i001",
                        "Price": 100,
                        "Quantity": 1,
                        "TaxCode": "T1"
                    }
                ]
            }
        }
        ```
        """
        return self._adapter.post("CreditNotesService_GetApprovalTemplates", data=payload)

    def handle_approval_request(self, payload: dict | None = None) -> Any:
        """POST CreditNotesService_HandleApprovalRequest
        Invoke the method 'HandleApprovalRequest' on this service.
        """
        return self._adapter.post("CreditNotesService_HandleApprovalRequest", data=payload)

    def init_data(self, payload: dict | None = None) -> Any:
        """POST CreditNotesService_InitData
        """
        return self._adapter.post("CreditNotesService_InitData", data=payload)

    def request_approve_cancellation(self, payload: dict | None = None) -> Any:
        """POST CreditNotesService_RequestApproveCancellation
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
        return self._adapter.post("CreditNotesService_RequestApproveCancellation", data=payload)
