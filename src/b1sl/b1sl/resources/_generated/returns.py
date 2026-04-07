from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ReturnsService(GenericResource["Document"]):
    """This entity enables you to manipulate 'Returns'. A return is the clearing document for a delivery."""
    endpoint = "Returns"
    
    def __init__(self, adapter):
        from ...models._generated._types import Document
        self.model = Document
        super().__init__(adapter)
