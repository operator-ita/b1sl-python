from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class SalesTaxInvoicesService(GenericResource["SalesTaxInvoice"]):
    """This entity enables you to manipulate 'SalesTaxInvoices'. It represents the data of a sales Tax Invoice document."""
    endpoint = "SalesTaxInvoices"
    
    def __init__(self, adapter):
        from ...models._generated._types import SalesTaxInvoice
        self.model = SalesTaxInvoice
        super().__init__(adapter)
