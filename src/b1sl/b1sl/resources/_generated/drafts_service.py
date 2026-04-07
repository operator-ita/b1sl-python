from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class DraftsService(GenericResource[Any]):
    endpoint = "DraftsService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def approve_and_add(self, payload: dict | None = None) -> Any:
        """POST DraftsService_ApproveAndAdd
        """
        return self._adapter.post("DraftsService_ApproveAndAdd", data=payload)

    def approve_and_update(self, payload: dict | None = None) -> Any:
        """POST DraftsService_ApproveAndUpdate
        """
        return self._adapter.post("DraftsService_ApproveAndUpdate", data=payload)

    def close_by_date(self, payload: dict | None = None) -> Any:
        """POST DraftsService_CloseByDate
        """
        return self._adapter.post("DraftsService_CloseByDate", data=payload)

    def export_e_way_bill(self, payload: dict | None = None) -> Any:
        """POST DraftsService_ExportEWayBill
        """
        return self._adapter.post("DraftsService_ExportEWayBill", data=payload)

    def get_approval_templates(self, payload: dict | None = None) -> Any:
        """POST DraftsService_GetApprovalTemplates
        Invoke the method 'GetApprovalTemplates' on this service by specifying the payload 'Document' in the JSON format.

        Example:
        ```json
        {
            "Document": {
                "CardCode": "c001",
                "DocObjectCode": "23",
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
        return self._adapter.post("DraftsService_GetApprovalTemplates", data=payload)

    def handle_approval_request(self, payload: dict | None = None) -> Any:
        """POST DraftsService_HandleApprovalRequest
        Invoke the method 'HandleApprovalRequest' on this service.
        """
        return self._adapter.post("DraftsService_HandleApprovalRequest", data=payload)

    def init_data(self, payload: dict | None = None) -> Any:
        """POST DraftsService_InitData
        """
        return self._adapter.post("DraftsService_InitData", data=payload)

    def save_draft_to_document(self, payload: dict | None = None) -> Any:
        """POST DraftsService_SaveDraftToDocument
        Invoke the method 'SaveDraftToDocument' on this service by specifying the payload 'Document' in the JSON format.

        Example:
        ```json
        {
            "Document": {
                "DocDueDate": "2017-01-28",
                "DocEntry": "3"
            }
        }
        ```
        """
        return self._adapter.post("DraftsService_SaveDraftToDocument", data=payload)
