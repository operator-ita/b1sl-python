from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class PurchaseQuotationsService(GenericResource["Document"]):
    """This entity enables you to manipulate 'PurchaseQuotations'. It represents an invitation to a number of vendors to find the best offer for goods or services that you require."""
    endpoint = "PurchaseQuotations"
    
    def __init__(self, adapter):
        from ...models._generated._types import Document
        self.model = Document
        super().__init__(adapter)
