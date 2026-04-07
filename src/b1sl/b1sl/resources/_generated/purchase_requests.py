from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class PurchaseRequestsService(GenericResource["Document"]):
    """This entity enables you to manipulate 'PurchaseRequests'. It allows users and employees in an organization to initiate a purchasing process by submitting their needs for certain goods or services."""
    endpoint = "PurchaseRequests"

    def __init__(self, adapter):
        from ...models._generated._types import Document
        self.model = Document
        super().__init__(adapter)
