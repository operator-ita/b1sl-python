from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class TaxCodeDeterminationsTCDService(GenericResource["TaxCodeDeterminationTCD"]):
    """This entity enables you to manipulate 'TaxCodeDeterminationsTCD'."""
    endpoint = "TaxCodeDeterminationsTCD"
    
    def __init__(self, adapter):
        from ...models._generated._types import TaxCodeDeterminationTCD
        self.model = TaxCodeDeterminationTCD
        super().__init__(adapter)
