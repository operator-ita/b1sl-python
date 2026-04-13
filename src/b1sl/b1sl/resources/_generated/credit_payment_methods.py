from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CreditPaymentMethodsService(GenericResource["CreditPaymentMethod"]):
    """This entity enables you to manipulate 'CreditPaymentMethods'. It defines credit card payment methods."""
    endpoint = "CreditPaymentMethods"
    
    def __init__(self, adapter):
        from ...models._generated._types import CreditPaymentMethod
        self.model = CreditPaymentMethod
        super().__init__(adapter)
