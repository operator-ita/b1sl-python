from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ChangeLogsService(GenericResource[Any]):
    endpoint = "ChangeLogsService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_change_log(self, payload: dict | None = None) -> Any:
        """POST ChangeLogsService_GetChangeLog
        Invoke the method 'GetChangeLog' on this service by specifying the payload 'GetChangeLogParams' in the JSON format.

        Example:
        ```json
        {
            "GetChangeLogParams": {
                "Object": "clPurchaseOrders",
                "PrimaryKey": "7",
                "UDOObjectCode": "3"
            }
        }
        ```
        """
        return self._adapter.post("ChangeLogsService_GetChangeLog", data=payload)

    def get_change_log_differences(self, payload: dict | None = None) -> Any:
        """POST ChangeLogsService_GetChangeLogDifferences
        Invoke the method 'GetChangeLogDifferences' on this service by specifying the payload 'ShowDifferenceParams' in the JSON format.

        Example:
        ```json
        {
            "ShowDifferenceParams": {
                "LogInstance": 1,
                "LogInstance2": 2,
                "Object": "clPurchaseOrders",
                "PrimaryKey": "7",
                "UDOObjectCode": "3"
            }
        }
        ```
        """
        return self._adapter.post("ChangeLogsService_GetChangeLogDifferences", data=payload)
