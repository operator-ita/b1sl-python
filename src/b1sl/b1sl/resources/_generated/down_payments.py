from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class DownPaymentsService(GenericResource["Document"]):
    """This entity enables you to manipulate 'DownPayments'. It represents a document for ensuring that a customer is committed and will follow through with a placed order."""
    endpoint = "DownPayments"
    
    def __init__(self, adapter):
        from ...models._generated._types import Document
        self.model = Document
        super().__init__(adapter)
