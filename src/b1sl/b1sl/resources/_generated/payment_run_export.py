from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class PaymentRunExportService(GenericResource["PaymentRunExport"]):
    """This entity enables you to manipulate 'PaymentRunExport'. It allows you to export data of automatic payments for both incoming payments and outgoing payments to vendors."""
    endpoint = "PaymentRunExport"
    
    def __init__(self, adapter):
        from ...models._generated._types import PaymentRunExport
        self.model = PaymentRunExport
        super().__init__(adapter)
