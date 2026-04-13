from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class WithholdingTaxCodesService(GenericResource["WithholdingTaxCode"]):
    """This entity enables you to manipulate 'WithholdingTaxCodes'. It defines withholding tax codes that can be applied to business partners, payments, and documents."""
    endpoint = "WithholdingTaxCodes"
    
    def __init__(self, adapter):
        from ...models._generated._types import WithholdingTaxCode
        self.model = WithholdingTaxCode
        super().__init__(adapter)
