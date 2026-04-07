from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ApprovalTemplatesService(GenericResource[Any]):
    endpoint = "ApprovalTemplatesService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_approval_template_list(self, payload: dict | None = None) -> Any:
        """POST ApprovalTemplatesService_GetApprovalTemplateList
        Invoke the method 'GetApprovalTemplateList' on this service.
        """
        return self._adapter.post(f"ApprovalTemplatesService_GetApprovalTemplateList", data=payload)
