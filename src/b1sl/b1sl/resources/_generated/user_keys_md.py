from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class UserKeysMDService(GenericResource["UserKeysMD"]):
    """This entity enables you to manipulate 'UserKeysMD' and manage secondary keys to user tables."""
    endpoint = "UserKeysMD"

    def __init__(self, adapter):
        from ...models._generated._types import UserKeysMD
        self.model = UserKeysMD
        super().__init__(adapter)
