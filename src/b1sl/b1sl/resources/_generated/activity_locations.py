from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ActivityLocationsService(GenericResource["ActivityLocation"]):
    """This entity enables you to manipulate 'ActivityLocations'. It represents locations where activities with your business partners take place."""
    endpoint = "ActivityLocations"
    
    def __init__(self, adapter):
        from ...models._generated._types import ActivityLocation
        self.model = ActivityLocation
        super().__init__(adapter)
