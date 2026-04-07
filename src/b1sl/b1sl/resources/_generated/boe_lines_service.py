from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class BOELinesService(GenericResource[Any]):
    endpoint = "BOELinesService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_boe_line(self, payload: dict | None = None) -> Any:
        """POST BOELinesService_GetBOELine
        Invoke the method 'GetBOELine' on this service by specifying the payload 'BOELineParams' in the JSON format.

        Example:
        ```json
        {
            "BOELineParams": {
                "BOEKey": "1"
            }
        }
        ```
        """
        return self._adapter.post("BOELinesService_GetBOELine", data=payload)
