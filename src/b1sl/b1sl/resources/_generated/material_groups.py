from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class MaterialGroupsService(GenericResource["MaterialGroup"]):
    """This entity enables you to manipulate 'MaterialGroups'."""
    endpoint = "MaterialGroups"

    def __init__(self, adapter):
        from ...models._generated._types import MaterialGroup
        self.model = MaterialGroup
        super().__init__(adapter)
