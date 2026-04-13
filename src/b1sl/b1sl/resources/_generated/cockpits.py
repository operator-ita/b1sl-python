from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CockpitsService(GenericResource["Cockpit"]):
    """This entity enables you to manipulate 'Cockpits'."""
    endpoint = "Cockpits"
    
    def __init__(self, adapter):
        from ...models._generated._types import Cockpit
        self.model = Cockpit
        super().__init__(adapter)
