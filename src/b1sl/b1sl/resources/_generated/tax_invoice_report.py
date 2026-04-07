from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class TaxInvoiceReportService(GenericResource["TaxInvoiceReport"]):
    """This entity enables you to manipulate 'TaxInvoiceReport'."""
    endpoint = "TaxInvoiceReport"
    
    def __init__(self, adapter):
        from ...models._generated._types import TaxInvoiceReport
        self.model = TaxInvoiceReport
        super().__init__(adapter)
