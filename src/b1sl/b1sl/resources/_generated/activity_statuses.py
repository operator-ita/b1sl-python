from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ActivityStatusesService(GenericResource["ActivityStatus"]):
    """This entity enables you to manipulate 'ActivityStatuses'. It is a business object that enables to define statuses for Task type activities in the Business Partners module."""
    endpoint = "ActivityStatuses"

    def __init__(self, adapter):
        from ...models._generated._types import ActivityStatus
        self.model = ActivityStatus
        super().__init__(adapter)
