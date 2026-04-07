from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class PurchaseReturnsService(GenericResource["Document"]):
    """This entity enables you to manipulate 'PurchaseReturns'. It is used to return delivered goods to vendors or to reverse completely or partially a purchasing transaction for an item."""
    endpoint = "PurchaseReturns"
    
    def __init__(self, adapter):
        from ...models._generated._types import Document
        self.model = Document
        super().__init__(adapter)
