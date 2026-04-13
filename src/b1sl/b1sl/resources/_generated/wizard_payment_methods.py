from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class WizardPaymentMethodsService(GenericResource["WizardPaymentMethod"]):
    """This entity enables you to manipulate 'WizardPaymentMethods'. It defines various payment methods for various payment means (such as check, bank transfer, and in some localizations, bills of exchange) which can be used in payment wizard runs."""
    endpoint = "WizardPaymentMethods"
    
    def __init__(self, adapter):
        from ...models._generated._types import WizardPaymentMethod
        self.model = WizardPaymentMethod
        super().__init__(adapter)
