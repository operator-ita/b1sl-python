from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class FiscalPrinterService(GenericResource[Any]):
    endpoint = "FiscalPrinterService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_fiscal_printer_list(self, payload: dict | None = None) -> Any:
        """POST FiscalPrinterService_GetFiscalPrinterList
        Invoke the method 'GetFiscalPrinterList' on this service.
        """
        return self._adapter.post("FiscalPrinterService_GetFiscalPrinterList", data=payload)
