from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class UserObjectsMDService(GenericResource["UserObjectsMD"]):
    """This entity enables you to manipulate 'UserObjectsMD'. It represents the registration data settings, such as table name and supported services, of a user-defined object."""
    endpoint = "UserObjectsMD"

    def __init__(self, adapter):
        from ...models._generated._types import UserObjectsMD
        self.model = UserObjectsMD
        super().__init__(adapter)
