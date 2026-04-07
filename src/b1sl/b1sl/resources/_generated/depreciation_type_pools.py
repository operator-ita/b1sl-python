from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class DepreciationTypePoolsService(GenericResource["DepreciationTypePool"]):
    """This entity enables you to manipulate 'DepreciationTypePools'."""
    endpoint = "DepreciationTypePools"

    def __init__(self, adapter):
        from ...models._generated._types import DepreciationTypePool
        self.model = DepreciationTypePool
        super().__init__(adapter)
