from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class SalesStagesService(GenericResource["SalesStage"]):
    """This entity enables you to manipulate 'SalesStages'. It defines sales stages and the probability of closing a deal indicated by each stage. For example, you enter stage 1 by identifying a customer as a lead (prospective customer); if you define the closing percentage of this stage as 5%, it means that you estimate 5 out of 100 leads can be converted to customers who will place orders with you."""
    endpoint = "SalesStages"

    def __init__(self, adapter):
        from ...models._generated._types import SalesStage
        self.model = SalesStage
        super().__init__(adapter)
