from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class TargetGroupsService(GenericResource["TargetGroup"]):
    """This entity enables you to manipulate 'TargetGroups'."""
    endpoint = "TargetGroups"
    
    def __init__(self, adapter):
        from ...models._generated._types import TargetGroup
        self.model = TargetGroup
        super().__init__(adapter)
