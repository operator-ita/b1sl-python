from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ActivityTypesService(GenericResource["ActivityType"]):
    """This entity enables you to manipulate 'ActivityTypes'. You may have different activities with your business partners, for example, phone calls and meetings."""
    endpoint = "ActivityTypes"

    def __init__(self, adapter):
        from ...models._generated._types import ActivityType
        self.model = ActivityType
        super().__init__(adapter)
