from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class QueueService(GenericResource["Queue"]):
    """This entity enables you to manipulate 'Queue'. It represents the queues list in the Service module from which you can assign a queue member to a service call."""
    endpoint = "Queue"
    
    def __init__(self, adapter):
        from ...models._generated._types import Queue
        self.model = Queue
        super().__init__(adapter)
