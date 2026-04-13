from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CreditNotesService(GenericResource["Document"]):
    """This entity enables you to manipulate 'CreditNotes'. It is the clearing document for invoices and returns. If the goods were delivered to the customer and an invoice has already been created, you can partially or completely reverse the transaction by creating a credit note."""
    endpoint = "CreditNotes"
    
    def __init__(self, adapter):
        from ...models._generated._types import Document
        self.model = Document
        super().__init__(adapter)
