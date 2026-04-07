from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class PurchaseTaxInvoicesService(GenericResource["PurchaseTaxInvoice"]):
    """This entity enables you to manipulate 'PurchaseTaxInvoices'. It represents the data of a purchase Tax Invoice document."""
    endpoint = "PurchaseTaxInvoices"

    def __init__(self, adapter):
        from ...models._generated._types import PurchaseTaxInvoice
        self.model = PurchaseTaxInvoice
        super().__init__(adapter)
