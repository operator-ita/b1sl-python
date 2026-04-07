from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class BankStatementsService(GenericResource[Any]):
    endpoint = "BankStatementsService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_bank_statement_list(self, payload: dict | None = None) -> Any:
        """POST BankStatementsService_GetBankStatementList
        Invoke the method 'GetBankStatementList' on this service by specifying the payload 'BankStatementsFilter' in the JSON format.

        Example:
        ```json
        {
            "BankStatementsFilter": {
                "Account": "111",
                "Bank": "10000000",
                "Country": "DE"
            }
        }
        ```
        """
        return self._adapter.post("BankStatementsService_GetBankStatementList", data=payload)
