from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class EmployeeTransfersService(GenericResource["EmployeeTransfer"]):
    """This entity enables you to manipulate 'EmployeeTransfers'."""
    endpoint = "EmployeeTransfers"
    
    def __init__(self, adapter):
        from ...models._generated._types import EmployeeTransfer
        self.model = EmployeeTransfer
        super().__init__(adapter)
