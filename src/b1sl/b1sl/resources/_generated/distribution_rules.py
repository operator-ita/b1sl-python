from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class DistributionRulesService(GenericResource["DistributionRule"]):
    """This entity enables you to manipulate 'DistributionRules'."""
    endpoint = "DistributionRules"
    
    def __init__(self, adapter):
        from ...models._generated._types import DistributionRule
        self.model = DistributionRule
        super().__init__(adapter)
