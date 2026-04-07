from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class PurchaseOrdersService(GenericResource["Document"]):
    """This entity enables you to manipulate 'PurchaseOrders'. It is a document used to request items or services from a vendor at an agreed upon price."""
    endpoint = "PurchaseOrders"

    def __init__(self, adapter):
        from ...models._generated._types import Document
        self.model = Document
        super().__init__(adapter)
