from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ServiceTaxPostingService(GenericResource[Any]):
    endpoint = "ServiceTaxPostingService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_taxable_deliveries(self, payload: dict | None = None) -> Any:
        """POST ServiceTaxPostingService_GetTaxableDeliveries
        Invoke the method 'GetTaxableDeliveries' on this service.
        """
        return self._adapter.post("ServiceTaxPostingService_GetTaxableDeliveries", data=payload)

    def post_service_tax(self, payload: dict | None = None) -> Any:
        """POST ServiceTaxPostingService_PostServiceTax
        Invoke the method 'PostServiceTax' on this service by specifying the payload 'ServiceTaxPostingParams' in the JSON format.

        Example:
        ```json
        {
            "ServiceTaxPostingParams": {
                "DocEntry": 5
            }
        }
        ```
        """
        return self._adapter.post("ServiceTaxPostingService_PostServiceTax", data=payload)
