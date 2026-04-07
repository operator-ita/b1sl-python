from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class FiscalPrinterService(GenericResource["FiscalPrinter"]):
    """This entity enables you to manipulate 'FiscalPrinter'."""
    endpoint = "FiscalPrinter"

    def __init__(self, adapter):
        from ...models._generated._types import FiscalPrinter
        self.model = FiscalPrinter
        super().__init__(adapter)
