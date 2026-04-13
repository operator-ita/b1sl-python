from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class AssetRetirementService(GenericResource["AssetDocument"]):
    """This entity enables you to manipulate 'AssetRetirement'."""
    endpoint = "AssetRetirement"
    
    def __init__(self, adapter):
        from ...models._generated._types import AssetDocument
        self.model = AssetDocument
        super().__init__(adapter)
