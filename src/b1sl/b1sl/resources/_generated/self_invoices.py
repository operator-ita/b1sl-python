from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class SelfInvoicesService(GenericResource["Document"]):
    """This entity enables you to manipulate 'SelfInvoices'. It represents a request for payment. It also records the cost in a profit and loss statement."""
    endpoint = "SelfInvoices"
    
    def __init__(self, adapter):
        from ...models._generated._types import Document
        self.model = Document
        super().__init__(adapter)
