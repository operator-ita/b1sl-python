from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class BPOpeningBalanceService(GenericResource[Any]):
    endpoint = "BPOpeningBalanceService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def create_open_balance(self, payload: dict | None = None) -> Any:
        """POST BPOpeningBalanceService_CreateOpenBalance
        Invoke the method 'CreateOpenBalance' on this service by specifying the payload 'OpenningBalanceAccount,BPCodes' in the JSON format.

        Example:
        ```json
        {
            "BPCodes": [
                {
                    "Code": "C01",
                    "Debit": "1000"
                },
                {
                    "Code": "V01",
                    "Debit": "1000"
                }
            ],
            "OpenningBalanceAccount": {
                "Details": "Transfer balance to BP",
                "OpenBalanceAccount": "999100"
            }
        }
        ```
        """
        return self._adapter.post("BPOpeningBalanceService_CreateOpenBalance", data=payload)
