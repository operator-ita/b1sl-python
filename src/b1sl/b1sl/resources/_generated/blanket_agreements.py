from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class BlanketAgreementsService(GenericResource["BlanketAgreement"]):
    """This entity enables you to manipulate 'BlanketAgreements'."""
    endpoint = "BlanketAgreements"
    
    def __init__(self, adapter):
        from ...models._generated._types import BlanketAgreement
        self.model = BlanketAgreement
        super().__init__(adapter)
