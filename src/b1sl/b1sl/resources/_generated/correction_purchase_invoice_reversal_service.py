from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CorrectionPurchaseInvoiceReversalService(GenericResource[Any]):
    endpoint = "CorrectionPurchaseInvoiceReversalService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def approve_and_add(self, payload: dict | None = None) -> Any:
        """POST CorrectionPurchaseInvoiceReversalService_ApproveAndAdd
        """
        return self._adapter.post(f"CorrectionPurchaseInvoiceReversalService_ApproveAndAdd", data=payload)

    def approve_and_update(self, payload: dict | None = None) -> Any:
        """POST CorrectionPurchaseInvoiceReversalService_ApproveAndUpdate
        """
        return self._adapter.post(f"CorrectionPurchaseInvoiceReversalService_ApproveAndUpdate", data=payload)

    def close_by_date(self, payload: dict | None = None) -> Any:
        """POST CorrectionPurchaseInvoiceReversalService_CloseByDate
        """
        return self._adapter.post(f"CorrectionPurchaseInvoiceReversalService_CloseByDate", data=payload)

    def export_e_way_bill(self, payload: dict | None = None) -> Any:
        """POST CorrectionPurchaseInvoiceReversalService_ExportEWayBill
        """
        return self._adapter.post(f"CorrectionPurchaseInvoiceReversalService_ExportEWayBill", data=payload)

    def get_approval_templates(self, payload: dict | None = None) -> Any:
        """POST CorrectionPurchaseInvoiceReversalService_GetApprovalTemplates
        Invoke the method 'GetApprovalTemplates' on this service by specifying the payload 'Document' in the JSON format.

        Example:
        ```json
        {
            "Document": {
                "CardCode": "v001",
                "Comments": "add correction invoice reversal based on correction invoice",
                "DocDate": "2014-12-06",
                "DocDueDate": "2014-12-06",
                "InternalCorrectedDocNum": "8"
            }
        }
        ```
        """
        return self._adapter.post(f"CorrectionPurchaseInvoiceReversalService_GetApprovalTemplates", data=payload)

    def handle_approval_request(self, payload: dict | None = None) -> Any:
        """POST CorrectionPurchaseInvoiceReversalService_HandleApprovalRequest
        Invoke the method 'HandleApprovalRequest' on this service.
        """
        return self._adapter.post(f"CorrectionPurchaseInvoiceReversalService_HandleApprovalRequest", data=payload)

    def init_data(self, payload: dict | None = None) -> Any:
        """POST CorrectionPurchaseInvoiceReversalService_InitData
        """
        return self._adapter.post(f"CorrectionPurchaseInvoiceReversalService_InitData", data=payload)
