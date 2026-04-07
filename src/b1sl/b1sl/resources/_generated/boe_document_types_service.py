from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class BOEDocumentTypesService(GenericResource[Any]):
    endpoint = "BOEDocumentTypesService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_boe_document_type_list(self, payload: dict | None = None) -> Any:
        """POST BOEDocumentTypesService_GetBOEDocumentTypeList
        Invoke the method 'GetBOEDocumentTypeList' on this service.
        """
        return self._adapter.post("BOEDocumentTypesService_GetBOEDocumentTypeList", data=payload)
