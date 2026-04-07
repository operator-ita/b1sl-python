from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class TSRExceptionalEventsService(GenericResource["TSRExceptionalEvent"]):
    """This entity enables you to manipulate 'TSRExceptionalEvents'."""
    endpoint = "TSRExceptionalEvents"
    
    def __init__(self, adapter):
        from ...models._generated._types import TSRExceptionalEvent
        self.model = TSRExceptionalEvent
        super().__init__(adapter)
