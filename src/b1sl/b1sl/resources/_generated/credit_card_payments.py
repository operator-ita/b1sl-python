from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CreditCardPaymentsService(GenericResource["CreditCardPayment"]):
    """This entity enables you to manipulate 'CreditCardPayments'. It defines dates on which the credit card company credits the cardholder."""
    endpoint = "CreditCardPayments"

    def __init__(self, adapter):
        from ...models._generated._types import CreditCardPayment
        self.model = CreditCardPayment
        super().__init__(adapter)
