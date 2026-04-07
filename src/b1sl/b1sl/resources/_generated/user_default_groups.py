from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class UserDefaultGroupsService(GenericResource["UserDefaultGroup"]):
    """This entity enables you to manipulate 'UserDefaultGroups'. It defines default values (such as, default documents, default address in printed documents, windows color, and so on)."""
    endpoint = "UserDefaultGroups"
    
    def __init__(self, adapter):
        from ...models._generated._types import UserDefaultGroup
        self.model = UserDefaultGroup
        super().__init__(adapter)
