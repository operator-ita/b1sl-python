from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class EnhancedDiscountGroupsService(GenericResource["EnhancedDiscountGroup"]):
    """This entity enables you to manipulate 'EnhancedDiscountGroups'."""
    endpoint = "EnhancedDiscountGroups"

    def __init__(self, adapter):
        from ...models._generated._types import EnhancedDiscountGroup
        self.model = EnhancedDiscountGroup
        super().__init__(adapter)
