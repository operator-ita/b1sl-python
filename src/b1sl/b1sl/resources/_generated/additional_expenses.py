from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class AdditionalExpensesService(GenericResource["AdditionalExpense"]):
    """This entity enables you to manipulate 'AdditionalExpenses'. It represents additional expenses for transporting freight or delivering services, such as delivery fees and tax deposits."""
    endpoint = "AdditionalExpenses"

    def __init__(self, adapter):
        from ...models._generated._types import AdditionalExpense
        self.model = AdditionalExpense
        super().__init__(adapter)
