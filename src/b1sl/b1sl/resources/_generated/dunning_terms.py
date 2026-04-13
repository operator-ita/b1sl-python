from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class DunningTermsService(GenericResource["DunningTerm"]):
    """This entity enables you to manipulate 'DunningTerms'."""
    endpoint = "DunningTerms"
    
    def __init__(self, adapter):
        from ...models._generated._types import DunningTerm
        self.model = DunningTerm
        super().__init__(adapter)
