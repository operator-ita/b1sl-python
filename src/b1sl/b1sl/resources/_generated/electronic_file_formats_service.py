from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ElectronicFileFormatsService(GenericResource[Any]):
    endpoint = "ElectronicFileFormatsService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_electronic_file_format_list(self, payload: dict | None = None) -> Any:
        """POST ElectronicFileFormatsService_GetElectronicFileFormatList
        Invoke the method 'GetElectronicFileFormatList' on this service.
        """
        return self._adapter.post("ElectronicFileFormatsService_GetElectronicFileFormatList", data=payload)
