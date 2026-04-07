from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CreditLinesService(GenericResource[Any]):
    endpoint = "CreditLinesService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_credit_line(self, payload: dict | None = None) -> Any:
        """POST CreditLinesService_GetCreditLine
        Invoke the method 'GetCreditLine' on this service by specifying the payload 'CreditLineParams' in the JSON format.

        Example:
        ```json
        {
            "CreditLinesParams": [
                {
                    "AbsId": 1
                }
            ]
        }
        ```
        """
        return self._adapter.post("CreditLinesService_GetCreditLine", data=payload)

    def get_valid_credit_line_list(self, payload: dict | None = None) -> Any:
        """POST CreditLinesService_GetValidCreditLineList
        Invoke the method 'GetValidCreditLineList' on this service.
        """
        return self._adapter.post("CreditLinesService_GetValidCreditLineList", data=payload)
