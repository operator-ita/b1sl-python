from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CorrectionInvoiceReversalService(GenericResource[Any]):
    endpoint = "CorrectionInvoiceReversalService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def approve_and_add(self, payload: dict | None = None) -> Any:
        """POST CorrectionInvoiceReversalService_ApproveAndAdd
        """
        return self._adapter.post("CorrectionInvoiceReversalService_ApproveAndAdd", data=payload)

    def approve_and_update(self, payload: dict | None = None) -> Any:
        """POST CorrectionInvoiceReversalService_ApproveAndUpdate
        """
        return self._adapter.post("CorrectionInvoiceReversalService_ApproveAndUpdate", data=payload)

    def close_by_date(self, payload: dict | None = None) -> Any:
        """POST CorrectionInvoiceReversalService_CloseByDate
        """
        return self._adapter.post("CorrectionInvoiceReversalService_CloseByDate", data=payload)

    def export_e_way_bill(self, payload: dict | None = None) -> Any:
        """POST CorrectionInvoiceReversalService_ExportEWayBill
        """
        return self._adapter.post("CorrectionInvoiceReversalService_ExportEWayBill", data=payload)

    def get_approval_templates(self, payload: dict | None = None) -> Any:
        """POST CorrectionInvoiceReversalService_GetApprovalTemplates
        Invoke the method 'GetApprovalTemplates' on this service by specifying the payload 'Document' in the JSON format.

        Example:
        ```json
        {
            "Document": {
                "CardCode": "c001",
                "Comments": "add correction invoice reversal based on correction invoice",
                "DocDate": "2014-12-06",
                "DocDueDate": "2014-12-06",
                "InternalCorrectedDocNum": "10"
            }
        }
        ```
        """
        return self._adapter.post("CorrectionInvoiceReversalService_GetApprovalTemplates", data=payload)

    def handle_approval_request(self, payload: dict | None = None) -> Any:
        """POST CorrectionInvoiceReversalService_HandleApprovalRequest
        Invoke the method 'HandleApprovalRequest' on this service.
        """
        return self._adapter.post("CorrectionInvoiceReversalService_HandleApprovalRequest", data=payload)

    def init_data(self, payload: dict | None = None) -> Any:
        """POST CorrectionInvoiceReversalService_InitData
        """
        return self._adapter.post("CorrectionInvoiceReversalService_InitData", data=payload)
