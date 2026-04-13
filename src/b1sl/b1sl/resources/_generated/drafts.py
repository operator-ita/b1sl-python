from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class DraftsService(GenericResource["Document"]):
    """This entity enables you to manipulate 'Drafts'. It is the preliminary version of a document or report."""
    endpoint = "Drafts"
    
    def __init__(self, adapter):
        from ...models._generated._types import Document
        self.model = Document
        super().__init__(adapter)
