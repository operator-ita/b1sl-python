from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CorrectionPurchaseInvoiceService(GenericResource[Any]):
    endpoint = "CorrectionPurchaseInvoiceService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def approve_and_add(self, payload: dict | None = None) -> Any:
        """POST CorrectionPurchaseInvoiceService_ApproveAndAdd
        """
        return self._adapter.post("CorrectionPurchaseInvoiceService_ApproveAndAdd", data=payload)

    def approve_and_update(self, payload: dict | None = None) -> Any:
        """POST CorrectionPurchaseInvoiceService_ApproveAndUpdate
        """
        return self._adapter.post("CorrectionPurchaseInvoiceService_ApproveAndUpdate", data=payload)

    def close_by_date(self, payload: dict | None = None) -> Any:
        """POST CorrectionPurchaseInvoiceService_CloseByDate
        """
        return self._adapter.post("CorrectionPurchaseInvoiceService_CloseByDate", data=payload)

    def export_e_way_bill(self, payload: dict | None = None) -> Any:
        """POST CorrectionPurchaseInvoiceService_ExportEWayBill
        """
        return self._adapter.post("CorrectionPurchaseInvoiceService_ExportEWayBill", data=payload)

    def get_approval_templates(self, payload: dict | None = None) -> Any:
        """POST CorrectionPurchaseInvoiceService_GetApprovalTemplates
        Invoke the method 'GetApprovalTemplates' on this service by specifying the payload 'Document' in the JSON format.

        Example:
        ```json
        {
            "Document": {
                "CardCode": "v001",
                "Comments": "Added by Service Layer",
                "DocumentLines": [
                    {
                        "CorrectionInvoiceItem": "ciis_ShouldBe",
                        "ItemCode": "item01",
                        "Price": "310",
                        "Quantity": "10",
                        "VatGroup": "B4"
                    },
                    {
                        "CorrectionInvoiceItem": "ciis_Was",
                        "ItemCode": "item01",
                        "Price": "110",
                        "Quantity": "10",
                        "VatGroup": "B4"
                    }
                ]
            }
        }
        ```
        """
        return self._adapter.post("CorrectionPurchaseInvoiceService_GetApprovalTemplates", data=payload)

    def handle_approval_request(self, payload: dict | None = None) -> Any:
        """POST CorrectionPurchaseInvoiceService_HandleApprovalRequest
        Invoke the method 'HandleApprovalRequest' on this service.
        """
        return self._adapter.post("CorrectionPurchaseInvoiceService_HandleApprovalRequest", data=payload)

    def init_data(self, payload: dict | None = None) -> Any:
        """POST CorrectionPurchaseInvoiceService_InitData
        """
        return self._adapter.post("CorrectionPurchaseInvoiceService_InitData", data=payload)
