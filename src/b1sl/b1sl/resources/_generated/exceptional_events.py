from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ExceptionalEventsService(GenericResource["ExceptionalEvent"]):
    """This entity enables you to manipulate 'ExceptionalEvents'."""
    endpoint = "ExceptionalEvents"
    
    def __init__(self, adapter):
        from ...models._generated._types import ExceptionalEvent
        self.model = ExceptionalEvent
        super().__init__(adapter)
