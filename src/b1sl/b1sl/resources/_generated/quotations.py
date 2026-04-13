from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class QuotationsService(GenericResource["Document"]):
    """This entity enables you to manipulate 'Quotations'. It is an offer or proposal that you send either to a customer or to a lead."""
    endpoint = "Quotations"
    
    def __init__(self, adapter):
        from ...models._generated._types import Document
        self.model = Document
        super().__init__(adapter)
