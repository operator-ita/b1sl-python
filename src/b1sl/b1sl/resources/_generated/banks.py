from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class BanksService(GenericResource["Bank"]):
    """This entity enables you to manipulate 'Banks'."""
    endpoint = "Banks"
    
    def __init__(self, adapter):
        from ...models._generated._types import Bank
        self.model = Bank
        super().__init__(adapter)
