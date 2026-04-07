from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class SalesOpportunitiesService(GenericResource["SalesOpportunities"]):
    """This entity enables you to manipulate 'SalesOpportunities'. It represents the data of sales opportunities in SAP Business One. Sales opportunities include potential sale volumes that may arise from business with customers and interested parties."""
    endpoint = "SalesOpportunities"

    def __init__(self, adapter):
        from ...models._generated._types import SalesOpportunities
        self.model = SalesOpportunities
        super().__init__(adapter)
