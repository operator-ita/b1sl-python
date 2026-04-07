from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class TaxCodeDeterminationsService(GenericResource[Any]):
    endpoint = "TaxCodeDeterminationsService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_tax_code_determination_list(self, payload: dict | None = None) -> Any:
        """POST TaxCodeDeterminationsService_GetTaxCodeDeterminationList
        Invoke the method 'GetTaxCodeDeterminationList' on this service.
        """
        return self._adapter.post("TaxCodeDeterminationsService_GetTaxCodeDeterminationList", data=payload)
