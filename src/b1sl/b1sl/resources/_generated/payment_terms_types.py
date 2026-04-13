from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class PaymentTermsTypesService(GenericResource["PaymentTermsType"]):
    """This entity enables you to manipulate 'PaymentTermsTypes'. It represents the types of payment terms in the Banking module. The payment terms define typical agreements that apply to transactions with customers and vendors."""
    endpoint = "PaymentTermsTypes"
    
    def __init__(self, adapter):
        from ...models._generated._types import PaymentTermsType
        self.model = PaymentTermsType
        super().__init__(adapter)
