from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class UserTablesMDService(GenericResource["UserTablesMD"]):
    """This entity enables you to manipulate 'UserTablesMD'."""
    endpoint = "UserTablesMD"

    def __init__(self, adapter):
        from ...models._generated._types import UserTablesMD
        self.model = UserTablesMD
        super().__init__(adapter)
