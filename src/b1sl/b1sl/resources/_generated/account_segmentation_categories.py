from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class AccountSegmentationCategoriesService(GenericResource["AccountSegmentationCategory"]):
    """This entity enables you to manipulate 'AccountSegmentationCategories'. It represents the categories under each of the account segments."""
    endpoint = "AccountSegmentationCategories"

    def __init__(self, adapter):
        from ...models._generated._types import AccountSegmentationCategory
        self.model = AccountSegmentationCategory
        super().__init__(adapter)
