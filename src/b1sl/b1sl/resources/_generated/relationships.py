from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class RelationshipsService(GenericResource["Relationship"]):
    """This entity enables you to manipulate 'Relationships'. It represents the relationships list from which a relationship definition can be associated with a partner in a sales opportunity."""
    endpoint = "Relationships"

    def __init__(self, adapter):
        from ...models._generated._types import Relationship
        self.model = Relationship
        super().__init__(adapter)
