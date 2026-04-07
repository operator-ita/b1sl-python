from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class SalesOpportunityInterestsSetupService(GenericResource["SalesOpportunityInterestSetup"]):
    """This entity enables you to manipulate 'SalesOpportunityInterestsSetup'."""
    endpoint = "SalesOpportunityInterestsSetup"

    def __init__(self, adapter):
        from ...models._generated._types import SalesOpportunityInterestSetup
        self.model = SalesOpportunityInterestSetup
        super().__init__(adapter)
