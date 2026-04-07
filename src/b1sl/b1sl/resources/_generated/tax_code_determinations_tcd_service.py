from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class TaxCodeDeterminationsTCDService(GenericResource[Any]):
    endpoint = "TaxCodeDeterminationsTCDService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_tax_code_determination_tcd_list(self, payload: dict | None = None) -> Any:
        """POST TaxCodeDeterminationsTCDService_GetTaxCodeDeterminationTCDList
        Invoke the method 'GetTaxCodeDeterminationTCDList' on this service.
        """
        return self._adapter.post("TaxCodeDeterminationsTCDService_GetTaxCodeDeterminationTCDList", data=payload)
