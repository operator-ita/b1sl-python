from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ProjectManagementTimeSheetService(GenericResource["PM_TimeSheetData"]):
    """This entity enables you to manipulate 'ProjectManagementTimeSheet'."""
    endpoint = "ProjectManagementTimeSheet"

    def __init__(self, adapter):
        from ...models._generated._types import PM_TimeSheetData
        self.model = PM_TimeSheetData
        super().__init__(adapter)
