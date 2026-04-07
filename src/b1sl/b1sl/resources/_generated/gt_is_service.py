from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class GTIsService(GenericResource[Any]):
    endpoint = "GTIsService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def import_(self, payload: dict | None = None) -> Any:
        """POST GTIsService_Import
        Invoke the method 'Import' on this service by specifying the payload 'GTIParams' in the JSON format.

        Example:
        ```json
        {
            "GTIParams": {}
        }
        ```
        """
        return self._adapter.post(f"GTIsService_Import", data=payload)
