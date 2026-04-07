from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class AccountsService(GenericResource[Any]):
    endpoint = "AccountsService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def create_open_balance(self, payload: dict | None = None) -> Any:
        """POST AccountsService_CreateOpenBalance
        Invoke the method 'CreateOpenBalance' on this service by specifying the payload 'OpenningBalanceAccount,GLAccounts' in the JSON format.

        Example:
        ```json
        {
            "GLAccounts": {
                "Code": "test"
            },
            "OpenningBalanceAccount": {
                "Date": "2016-08-29"
            }
        }
        ```
        """
        return self._adapter.post("AccountsService_CreateOpenBalance", data=payload)
