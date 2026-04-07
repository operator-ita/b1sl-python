from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class MessagesService(GenericResource[Any]):
    endpoint = "MessagesService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_sent_messages(self, payload: dict | None = None) -> Any:
        """POST MessagesService_GetSentMessages
        Invoke the method 'GetSentMessages' on this service.
        """
        return self._adapter.post("MessagesService_GetSentMessages", data=payload)

    # --- Functions ---

    def get_inbox(self, params: dict | None = None) -> Any:
        """POST MessagesService_GetInbox(params)
        Invoke the method 'GetInbox' on this service.
        """
        return self._function("MessagesService_GetInbox", params)

    def get_outbox(self, params: dict | None = None) -> Any:
        """POST MessagesService_GetOutbox(params)
        Invoke the method 'GetOutbox' on this service.
        """
        return self._function("MessagesService_GetOutbox", params)
