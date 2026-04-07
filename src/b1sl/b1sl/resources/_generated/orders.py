from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class OrdersService(GenericResource["Document"]):
    """This entity enables you to manipulate 'Orders'. It represents a commitment from a customer or lead to buy a product or service."""
    endpoint = "Orders"

    def __init__(self, adapter):
        from ...models._generated._types import Document
        self.model = Document
        super().__init__(adapter)
