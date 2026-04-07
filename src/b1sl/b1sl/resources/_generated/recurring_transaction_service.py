from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class RecurringTransactionService(GenericResource[Any]):
    endpoint = "RecurringTransactionService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def delete_recurring_transactions(self, payload: dict | None = None) -> Any:
        """POST RecurringTransactionService_DeleteRecurringTransactions
        Invoke the method 'DeleteRecurringTransactions' on this service by specifying the payload 'RclRecurringTransactionParamsCollection' in the JSON format.

        Example:
        ```json
        {
            "RclRecurringTransactionParamsCollection": [
                {},
                {}
            ]
        }
        ```
        """
        return self._adapter.post("RecurringTransactionService_DeleteRecurringTransactions", data=payload)

    def execute_recurring_transactions(self, payload: dict | None = None) -> Any:
        """POST RecurringTransactionService_ExecuteRecurringTransactions
        Invoke the method 'ExecuteRecurringTransactions' on this service by specifying the payload 'RclRecurringTransactionParamsCollection,RclRecurringExecutionParams' in the JSON format.

        Example:
        ```json
        {
            "RclRecurringExecutionParams": {},
            "RclRecurringTransactionParamsCollection": [
                {},
                {}
            ]
        }
        ```
        """
        return self._adapter.post("RecurringTransactionService_ExecuteRecurringTransactions", data=payload)

    def get_available_recurring_transactions(self, payload: dict | None = None) -> Any:
        """POST RecurringTransactionService_GetAvailableRecurringTransactions
        Invoke the method 'GetAvailableRecurringTransactions' on this service.
        """
        return self._adapter.post("RecurringTransactionService_GetAvailableRecurringTransactions", data=payload)

    def get_recurring_transaction(self, payload: dict | None = None) -> Any:
        """POST RecurringTransactionService_GetRecurringTransaction
        Invoke the method 'GetRecurringTransaction' on this service by specifying the payload 'RclRecurringTransactionParams' in the JSON format.

        Example:
        ```json
        {
            "RclRecurringTransactionParams": {}
        }
        ```
        """
        return self._adapter.post("RecurringTransactionService_GetRecurringTransaction", data=payload)
