from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ExtendedTranslationsService(GenericResource[Any]):
    endpoint = "ExtendedTranslationsService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_extended_translation_list(self, payload: dict | None = None) -> Any:
        """POST ExtendedTranslationsService_GetExtendedTranslationList
        Invoke the method 'GetExtendedTranslationList' on this service.
        """
        return self._adapter.post("ExtendedTranslationsService_GetExtendedTranslationList", data=payload)
