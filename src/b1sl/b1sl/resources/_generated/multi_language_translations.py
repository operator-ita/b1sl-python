from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class MultiLanguageTranslationsService(GenericResource["MultiLanguageTranslation"]):
    """This entity enables you to manipulate 'MultiLanguageTranslations'. It allows translating alphanumeric data of specified fields in master data objects (such as BusinessPartners and Items) to foreign languages and then printing documents in the translated languages."""
    endpoint = "MultiLanguageTranslations"
    
    def __init__(self, adapter):
        from ...models._generated._types import MultiLanguageTranslation
        self.model = MultiLanguageTranslation
        super().__init__(adapter)
