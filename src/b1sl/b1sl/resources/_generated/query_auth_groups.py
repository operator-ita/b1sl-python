from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class QueryAuthGroupsService(GenericResource["QueryAuthGroup"]):
    """This entity enables you to manipulate 'QueryAuthGroups'."""
    endpoint = "QueryAuthGroups"

    def __init__(self, adapter):
        from ...models._generated._types import QueryAuthGroup
        self.model = QueryAuthGroup
        super().__init__(adapter)
