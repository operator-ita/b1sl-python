from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class BOEDocumentTypesService(GenericResource["BOEDocumentType"]):
    """This entity enables you to manipulate 'BOEDocumentTypes'."""
    endpoint = "BOEDocumentTypes"
    
    def __init__(self, adapter):
        from ...models._generated._types import BOEDocumentType
        self.model = BOEDocumentType
        super().__init__(adapter)
