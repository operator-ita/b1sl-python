from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class StockTransferDraftService(GenericResource[Any]):
    endpoint = "StockTransferDraftService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_approval_templates(self, payload: dict | None = None) -> Any:
        """POST StockTransferDraftService_GetApprovalTemplates
        Invoke the method 'GetApprovalTemplates' on this service by specifying the payload 'StockTransfer' in the JSON format.

        Example:
        ```json
        {
            "StockTransfer": {}
        }
        ```
        """
        return self._adapter.post("StockTransferDraftService_GetApprovalTemplates", data=payload)

    def handle_approval_request(self, payload: dict | None = None) -> Any:
        """POST StockTransferDraftService_HandleApprovalRequest
        Invoke the method 'HandleApprovalRequest' on this service.
        """
        return self._adapter.post("StockTransferDraftService_HandleApprovalRequest", data=payload)
