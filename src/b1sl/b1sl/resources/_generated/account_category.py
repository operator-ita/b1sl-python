from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class AccountCategoryService(GenericResource["AccountCategory"]):
    """This entity enables you to manipulate 'AccountCategory'."""
    endpoint = "AccountCategory"

    def __init__(self, adapter):
        from ...models._generated._types import AccountCategory
        self.model = AccountCategory
        super().__init__(adapter)
