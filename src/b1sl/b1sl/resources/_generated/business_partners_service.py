from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class BusinessPartnersService(GenericResource[Any]):
    endpoint = "BusinessPartnersService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def create_open_balance(self, payload: dict | None = None) -> Any:
        """POST BusinessPartnersService_CreateOpenBalance
        Invoke the method 'CreateOpenBalance' on this service by specifying the payload 'OpenningBalanceAccount,BPCodes' in the JSON format.

        Example:
        ```json
        {
            "BPCodes": [
                {
                    "Code": "HU1006",
                    "Credit": 300
                },
                {
                    "Code": "HU1007",
                    "Credit": 300
                }
            ],
            "OpenningBalanceAccount": {
                "Date": "2016-09-19",
                "Details": "Bp Accounts Opening Balance",
                "OpenBalanceAccount": "_SYS00000000078"
            }
        }
        ```
        """
        return self._adapter.post(f"BusinessPartnersService_CreateOpenBalance", data=payload)

    def init_data(self, payload: dict | None = None) -> Any:
        """POST BusinessPartnersService_InitData
        """
        return self._adapter.post(f"BusinessPartnersService_InitData", data=payload)
