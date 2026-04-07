from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class IncomingPaymentsService(GenericResource["Payment"]):
    """This entity enables you to manipulate 'IncomingPayments'. It represents incoming payments from customers or, for returned goods, from vendors. Available payment methods are cash, credit cards, checks, bank transfers, and in some localizations, bills of exchange."""
    endpoint = "IncomingPayments"

    def __init__(self, adapter):
        from ...models._generated._types import Payment
        self.model = Payment
        super().__init__(adapter)
