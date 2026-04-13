from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class SalesTaxCodesService(GenericResource["SalesTaxCode"]):
    """This entity enables you to manipulate 'SalesTaxCodes'. It represents the inclusive sales tax codes. Each sales tax code consists of one or more sales taxes."""
    endpoint = "SalesTaxCodes"
    
    def __init__(self, adapter):
        from ...models._generated._types import SalesTaxCode
        self.model = SalesTaxCode
        super().__init__(adapter)
