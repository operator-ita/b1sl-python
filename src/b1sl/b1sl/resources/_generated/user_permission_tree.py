from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class UserPermissionTreeService(GenericResource["UserPermissionTree"]):
    """This entity enables you to manipulate 'UserPermissionTree'. It represents the User Authorization form. This object enables managing user authorization for various forms."""
    endpoint = "UserPermissionTree"

    def __init__(self, adapter):
        from ...models._generated._types import UserPermissionTree
        self.model = UserPermissionTree
        super().__init__(adapter)
