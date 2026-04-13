from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class EmployeesInfoService(GenericResource["EmployeeInfo"]):
    """This entity enables you to manipulate 'EmployeesInfo'."""
    endpoint = "EmployeesInfo"
    
    def __init__(self, adapter):
        from ...models._generated._types import EmployeeInfo
        self.model = EmployeeInfo
        super().__init__(adapter)
