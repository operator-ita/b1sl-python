from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class BOEInstructionsService(GenericResource[Any]):
    endpoint = "BOEInstructionsService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_boe_instruction_list(self, payload: dict | None = None) -> Any:
        """POST BOEInstructionsService_GetBOEInstructionList
        Invoke the method 'GetBOEInstructionList' on this service.
        """
        return self._adapter.post("BOEInstructionsService_GetBOEInstructionList", data=payload)
