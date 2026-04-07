from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class QueryCategoriesService(GenericResource["QueryCategory"]):
    """This entity enables you to manipulate 'QueryCategories'. It represents the predefined query categories."""
    endpoint = "QueryCategories"
    
    def __init__(self, adapter):
        from ...models._generated._types import QueryCategory
        self.model = QueryCategory
        super().__init__(adapter)
