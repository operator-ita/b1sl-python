from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class DepositsService(GenericResource[Any]):
    endpoint = "DepositsService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def cancel_check_row(self, payload: dict | None = None) -> Any:
        """POST DepositsService_CancelCheckRow
        Invoke the method 'CancelCheckRow' on this service by specifying the payload 'CancelCheckRowParams' in the JSON format.

        Example:
        ```json
        {
            "CancelCheckRowParams": {
                "CheckID": 1,
                "DepositID": 11
            }
        }
        ```
        """
        return self._adapter.post(f"DepositsService_CancelCheckRow", data=payload)

    def cancel_check_rowby_current_system_date(self, payload: dict | None = None) -> Any:
        """POST DepositsService_CancelCheckRowbyCurrentSystemDate
        Invoke the method 'CancelCheckRowbyCurrentSystemDate' on this service by specifying the payload 'CancelCheckRowParams' in the JSON format.

        Example:
        ```json
        {
            "CancelCheckRowParams": {
                "CheckID": 2,
                "DepositID": 11
            }
        }
        ```
        """
        return self._adapter.post(f"DepositsService_CancelCheckRowbyCurrentSystemDate", data=payload)

    def get_deposit_list(self, payload: dict | None = None) -> Any:
        """POST DepositsService_GetDepositList
        Invoke the method 'GetDepositList' on this service.
        """
        return self._adapter.post(f"DepositsService_GetDepositList", data=payload)
