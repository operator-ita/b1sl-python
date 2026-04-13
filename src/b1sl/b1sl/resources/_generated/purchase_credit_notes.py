from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class PurchaseCreditNotesService(GenericResource["Document"]):
    """This entity enables you to manipulate 'PurchaseCreditNotes'. It represents the clearing document for the A/P invoice. Therefore, if the vendor has delivered goods, and you have already created an A/P invoice, you can reverse the transaction either partially or completely by creating a purchase credit note."""
    endpoint = "PurchaseCreditNotes"
    
    def __init__(self, adapter):
        from ...models._generated._types import Document
        self.model = Document
        super().__init__(adapter)
