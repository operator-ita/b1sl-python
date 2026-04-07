from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class BudgetDistributionsService(GenericResource["BudgetDistribution"]):
    """This entity enables you to manipulate 'BudgetDistributions'."""
    endpoint = "BudgetDistributions"

    def __init__(self, adapter):
        from ...models._generated._types import BudgetDistribution
        self.model = BudgetDistribution
        super().__init__(adapter)
