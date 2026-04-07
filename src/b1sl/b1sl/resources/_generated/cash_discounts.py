from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CashDiscountsService(GenericResource["CashDiscount"]):
    """This entity enables you to manipulate 'CashDiscounts'."""
    endpoint = "CashDiscounts"

    def __init__(self, adapter):
        from ...models._generated._types import CashDiscount
        self.model = CashDiscount
        super().__init__(adapter)
