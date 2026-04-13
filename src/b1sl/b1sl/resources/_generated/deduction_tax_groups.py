from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class DeductionTaxGroupsService(GenericResource["DeductionTaxGroup"]):
    """This entity enables you to manipulate 'DeductionTaxGroups'. It represents withholding tax deduction groups."""
    endpoint = "DeductionTaxGroups"
    
    def __init__(self, adapter):
        from ...models._generated._types import DeductionTaxGroup
        self.model = DeductionTaxGroup
        super().__init__(adapter)
