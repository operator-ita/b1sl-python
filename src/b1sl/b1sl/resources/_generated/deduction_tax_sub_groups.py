from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class DeductionTaxSubGroupsService(GenericResource["DeductionTaxSubGroup"]):
    """This entity enables you to manipulate 'DeductionTaxSubGroups'."""
    endpoint = "DeductionTaxSubGroups"
    
    def __init__(self, adapter):
        from ...models._generated._types import DeductionTaxSubGroup
        self.model = DeductionTaxSubGroup
        super().__init__(adapter)
