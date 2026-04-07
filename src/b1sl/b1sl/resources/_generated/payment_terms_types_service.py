from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class PaymentTermsTypesService(GenericResource[Any]):
    endpoint = "PaymentTermsTypesService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def update_with_b_ps(self, payload: dict | None = None) -> Any:
        """POST PaymentTermsTypesService_UpdateWithBPs
        Invoke the method 'UpdateWithBPs' on this service by specifying the payload 'PaymentTermsType' in the JSON format.

        Example:
        ```json
        {
            "PaymentTermsType": {}
        }
        ```
        """
        return self._adapter.post(f"PaymentTermsTypesService_UpdateWithBPs", data=payload)
