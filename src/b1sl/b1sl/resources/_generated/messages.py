from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class MessagesService(GenericResource["Message"]):
    """This entity enables you to manipulate 'Messages'. You can also specify the OData query options to query the messages, which is a combination of Inbox messages, Outbox messages and to-send messages."""
    endpoint = "Messages"
    
    def __init__(self, adapter):
        from ...models._generated._types import Message
        self.model = Message
        super().__init__(adapter)
