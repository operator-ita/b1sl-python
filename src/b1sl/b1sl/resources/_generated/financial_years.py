from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class FinancialYearsService(GenericResource["FinancialYear"]):
    """This entity enables you to manipulate 'FinancialYears'."""
    endpoint = "FinancialYears"

    def __init__(self, adapter):
        from ...models._generated._types import FinancialYear
        self.model = FinancialYear
        super().__init__(adapter)
