from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class EmployeePositionService(GenericResource["EmployeePosition"]):
    """This entity enables you to manipulate 'EmployeePosition'."""
    endpoint = "EmployeePosition"

    def __init__(self, adapter):
        from ...models._generated._types import EmployeePosition
        self.model = EmployeePosition
        super().__init__(adapter)
