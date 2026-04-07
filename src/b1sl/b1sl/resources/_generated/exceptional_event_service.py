from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ExceptionalEventService(GenericResource[Any]):
    endpoint = "ExceptionalEventService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_exceptional_event_list(self, payload: dict | None = None) -> Any:
        """POST ExceptionalEventService_GetExceptionalEventList
        Invoke the method 'GetExceptionalEventList' on this service.
        """
        return self._adapter.post("ExceptionalEventService_GetExceptionalEventList", data=payload)
