from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class InternalReconciliationsService(GenericResource[Any]):
    endpoint = "InternalReconciliationsService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_open_transactions(self, payload: dict | None = None) -> Any:
        """POST InternalReconciliationsService_GetOpenTransactions
        Invoke the method 'GetOpenTransactions' on this service by specifying the payload 'InternalReconciliationOpenTransParams' in the JSON format.

        Example:
        ```json
        {
            "InternalReconciliationOpenTransParams": {
                "CardOrAccount": "coaCard",
                "InternalReconciliationBPs": [
                    {
                        "BPCode": "v01"
                    }
                ],
                "ReconDate": "2017-11-15"
            }
        }
        ```
        """
        return self._adapter.post("InternalReconciliationsService_GetOpenTransactions", data=payload)

    def request_approve_cancellation(self, payload: dict | None = None) -> Any:
        """POST InternalReconciliationsService_RequestApproveCancellation
        Invoke the method 'RequestApproveCancellation' on this service by specifying the payload 'InternalReconciliationParams' in the JSON format.

        Example:
        ```json
        {
            "InternalReconciliationParams": {
                "ReconNum": "4"
            }
        }
        ```
        """
        return self._adapter.post("InternalReconciliationsService_RequestApproveCancellation", data=payload)
