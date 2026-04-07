from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class NCMCodesSetupService(GenericResource[Any]):
    endpoint = "NCMCodesSetupService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_ncm_code_setup_list(self, payload: dict | None = None) -> Any:
        """POST NCMCodesSetupService_GetNCMCodeSetupList
        Invoke the method 'GetNCMCodeSetupList' on this service.
        """
        return self._adapter.post("NCMCodesSetupService_GetNCMCodeSetupList", data=payload)
