from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class AddressService(GenericResource[Any]):
    endpoint = "AddressService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_address_format(self, payload: dict | None = None) -> Any:
        """POST AddressService_GetAddressFormat
        """
        return self._adapter.post(f"AddressService_GetAddressFormat", data=payload)

    def get_full_address(self, payload: dict | None = None) -> Any:
        """POST AddressService_GetFullAddress
        Invoke the method 'GetFullAddress' on this service by specifying the payload 'AddressParams' in the JSON format.

        Example:
        ```json
        {
            "AddressParams": {
                "Block": "1001",
                "City": "Shanghai",
                "Country": "CN",
                "Street": "Chenhui"
            }
        }
        ```
        """
        return self._adapter.post(f"AddressService_GetFullAddress", data=payload)
