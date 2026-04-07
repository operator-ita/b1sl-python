from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class Attachments2Service(GenericResource["Attachments2"]):
    """This entity enables you to manipulate 'Attachments2'."""
    endpoint = "Attachments2"
    
    def __init__(self, adapter):
        from ...models._generated._types import Attachments2
        self.model = Attachments2
        super().__init__(adapter)
