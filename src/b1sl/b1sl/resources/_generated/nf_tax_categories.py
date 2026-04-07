from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class NFTaxCategoriesService(GenericResource["NFTaxCategory"]):
    """This entity enables you to manipulate 'NFTaxCategories'."""
    endpoint = "NFTaxCategories"

    def __init__(self, adapter):
        from ...models._generated._types import NFTaxCategory
        self.model = NFTaxCategory
        super().__init__(adapter)
