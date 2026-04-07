from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class KPIsService(GenericResource["KPI"]):
    """This entity enables you to manipulate 'KPIs'."""
    endpoint = "KPIs"

    def __init__(self, adapter):
        from ...models._generated._types import KPI
        self.model = KPI
        super().__init__(adapter)
