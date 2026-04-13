from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class DepreciationAreasService(GenericResource["DepreciationArea"]):
    """This entity enables you to manipulate 'DepreciationAreas'."""
    endpoint = "DepreciationAreas"
    
    def __init__(self, adapter):
        from ...models._generated._types import DepreciationArea
        self.model = DepreciationArea
        super().__init__(adapter)
