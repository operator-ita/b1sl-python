from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class AssetGroupsService(GenericResource["AssetGroup"]):
    """This entity enables you to manipulate 'AssetGroups'."""
    endpoint = "AssetGroups"

    def __init__(self, adapter):
        from ...models._generated._types import AssetGroup
        self.model = AssetGroup
        super().__init__(adapter)
