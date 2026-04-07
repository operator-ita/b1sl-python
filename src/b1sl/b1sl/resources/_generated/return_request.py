from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ReturnRequestService(GenericResource["Document"]):
    """This entity enables you to manipulate 'ReturnRequest'. A return is the clearing document for a delivery."""
    endpoint = "ReturnRequest"
    
    def __init__(self, adapter):
        from ...models._generated._types import Document
        self.model = Document
        super().__init__(adapter)
