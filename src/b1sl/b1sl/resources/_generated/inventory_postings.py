from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class InventoryPostingsService(GenericResource["InventoryPosting"]):
    """This entity enables you to manipulate 'InventoryPostings'."""
    endpoint = "InventoryPostings"

    def __init__(self, adapter):
        from ...models._generated._types import InventoryPosting
        self.model = InventoryPosting
        super().__init__(adapter)
