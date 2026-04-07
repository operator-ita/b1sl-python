from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class DeductibleTaxesService(GenericResource["DeductibleTax"]):
    """This entity enables you to manipulate 'DeductibleTaxes'."""
    endpoint = "DeductibleTaxes"
    
    def __init__(self, adapter):
        from ...models._generated._types import DeductibleTax
        self.model = DeductibleTax
        super().__init__(adapter)
