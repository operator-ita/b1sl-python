from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class MaterialRevaluationService(GenericResource["MaterialRevaluation"]):
    """This entity enables you to manipulate 'MaterialRevaluation'. It allows to update the items' price (average price or standard price only), revaluate the stock, and create journal entries accordingly."""
    endpoint = "MaterialRevaluation"
    
    def __init__(self, adapter):
        from ...models._generated._types import MaterialRevaluation
        self.model = MaterialRevaluation
        super().__init__(adapter)
