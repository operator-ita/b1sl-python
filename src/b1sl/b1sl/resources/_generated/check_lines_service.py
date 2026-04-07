from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CheckLinesService(GenericResource[Any]):
    endpoint = "CheckLinesService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_check_line(self, payload: dict | None = None) -> Any:
        """POST CheckLinesService_GetCheckLine
        Invoke the method 'GetCheckLine' on this service by specifying the payload 'CheckLineParams' in the JSON format.

        Example:
        ```json
        {
            "CheckLinesParams": [
                {
                    "CheckKey": 1
                }
            ]
        }
        ```
        """
        return self._adapter.post("CheckLinesService_GetCheckLine", data=payload)

    def get_valid_check_line_list(self, payload: dict | None = None) -> Any:
        """POST CheckLinesService_GetValidCheckLineList
        Invoke the method 'GetValidCheckLineList' on this service.
        """
        return self._adapter.post("CheckLinesService_GetValidCheckLineList", data=payload)
