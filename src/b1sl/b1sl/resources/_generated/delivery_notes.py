from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class DeliveryNotesService(GenericResource["Document"]):
    """This entity enables you to manipulate 'DeliveryNotes'. It is a legally binding document indicating that the shipment of goods or the delivery of services has occurred."""
    endpoint = "DeliveryNotes"
    
    def __init__(self, adapter):
        from ...models._generated._types import Document
        self.model = Document
        super().__init__(adapter)
