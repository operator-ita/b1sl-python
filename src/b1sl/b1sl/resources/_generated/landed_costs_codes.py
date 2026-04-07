from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class LandedCostsCodesService(GenericResource["LandedCostsCode"]):
    """This entity enables you to manipulate 'LandedCostsCodes'. It defines various types of landed costs (for example, insurance, customs) and their default distribution rules. When you record landed costs for deliveries, landed costs are allocated to the goods according to the distribution rule of each type."""
    endpoint = "LandedCostsCodes"
    
    def __init__(self, adapter):
        from ...models._generated._types import LandedCostsCode
        self.model = LandedCostsCode
        super().__init__(adapter)
