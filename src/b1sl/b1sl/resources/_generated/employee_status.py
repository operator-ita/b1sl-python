from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class EmployeeStatusService(GenericResource["EmployeeStatus"]):
    """This entity enables you to manipulate 'EmployeeStatus'."""
    endpoint = "EmployeeStatus"
    
    def __init__(self, adapter):
        from ...models._generated._types import EmployeeStatus
        self.model = EmployeeStatus
        super().__init__(adapter)
