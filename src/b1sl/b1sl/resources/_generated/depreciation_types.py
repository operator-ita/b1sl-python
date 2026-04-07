from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class DepreciationTypesService(GenericResource["DepreciationType"]):
    """This entity enables you to manipulate 'DepreciationTypes'."""
    endpoint = "DepreciationTypes"
    
    def __init__(self, adapter):
        from ...models._generated._types import DepreciationType
        self.model = DepreciationType
        super().__init__(adapter)
