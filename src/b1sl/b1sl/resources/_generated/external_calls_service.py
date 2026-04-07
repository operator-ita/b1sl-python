from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ExternalCallsService(GenericResource[Any]):
    endpoint = "ExternalCallsService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_call(self, payload: dict | None = None) -> Any:
        """POST ExternalCallsService_GetCall
        Invoke the method 'GetCall' on this service by specifying the payload 'ExternalCallParams' in the JSON format.

        Example:
        ```json
        {
            "ExternalCallParams": {}
        }
        ```
        """
        return self._adapter.post("ExternalCallsService_GetCall", data=payload)

    def send_call(self, payload: dict | None = None) -> Any:
        """POST ExternalCallsService_SendCall
        Invoke the method 'SendCall' on this service by specifying the payload 'ExternalCall' in the JSON format.

        Example:
        ```json
        {
            "ExternalCall": {}
        }
        ```
        """
        return self._adapter.post("ExternalCallsService_SendCall", data=payload)

    def update_call(self, payload: dict | None = None) -> Any:
        """POST ExternalCallsService_UpdateCall
        Invoke the method 'UpdateCall' on this service by specifying the payload 'ExternalCall' in the JSON format.

        Example:
        ```json
        {
            "ExternalCall": {}
        }
        ```
        """
        return self._adapter.post("ExternalCallsService_UpdateCall", data=payload)
