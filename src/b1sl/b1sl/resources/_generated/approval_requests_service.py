from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ApprovalRequestsService(GenericResource[Any]):
    endpoint = "ApprovalRequestsService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_all_approval_requests_list(self, payload: dict | None = None) -> Any:
        """POST ApprovalRequestsService_GetAllApprovalRequestsList
        Invoke the method 'GetAllApprovalRequestsList' on this service.
        """
        return self._adapter.post(f"ApprovalRequestsService_GetAllApprovalRequestsList", data=payload)

    def get_approval_request_list(self, payload: dict | None = None) -> Any:
        """POST ApprovalRequestsService_GetApprovalRequestList
        Invoke the method 'GetApprovalRequestList' on this service.
        """
        return self._adapter.post(f"ApprovalRequestsService_GetApprovalRequestList", data=payload)

    def get_open_approval_request_list(self, payload: dict | None = None) -> Any:
        """POST ApprovalRequestsService_GetOpenApprovalRequestList
        Invoke the method 'GetOpenApprovalRequestList' on this service.
        """
        return self._adapter.post(f"ApprovalRequestsService_GetOpenApprovalRequestList", data=payload)
