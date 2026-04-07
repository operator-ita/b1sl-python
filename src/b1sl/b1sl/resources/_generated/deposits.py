from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class DepositsService(GenericResource["Deposit"]):
    """This entity enables you to manipulate 'Deposits'."""
    endpoint = "Deposits"
    
    def __init__(self, adapter):
        from ...models._generated._types import Deposit
        self.model = Deposit
        super().__init__(adapter)
