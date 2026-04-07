from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class BranchesService(GenericResource[Any]):
    endpoint = "BranchesService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_branch_list(self, payload: dict | None = None) -> Any:
        """POST BranchesService_GetBranchList
        Invoke the method 'GetBranchList' on this service.
        """
        return self._adapter.post("BranchesService_GetBranchList", data=payload)
