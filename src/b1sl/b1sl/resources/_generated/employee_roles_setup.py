from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class EmployeeRolesSetupService(GenericResource["EmployeeRoleSetup"]):
    """This entity enables you to manipulate 'EmployeeRolesSetup'."""
    endpoint = "EmployeeRolesSetup"
    
    def __init__(self, adapter):
        from ...models._generated._types import EmployeeRoleSetup
        self.model = EmployeeRoleSetup
        super().__init__(adapter)
