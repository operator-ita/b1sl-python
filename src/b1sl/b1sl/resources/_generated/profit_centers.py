from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ProfitCentersService(GenericResource["ProfitCenter"]):
    """This entity enables you to manipulate 'ProfitCenters'."""
    endpoint = "ProfitCenters"

    def __init__(self, adapter):
        from ...models._generated._types import ProfitCenter
        self.model = ProfitCenter
        super().__init__(adapter)
