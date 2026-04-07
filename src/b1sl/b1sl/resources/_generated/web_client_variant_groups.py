from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class WebClientVariantGroupsService(GenericResource["WebClientVariantGroup"]):
    """This entity enables you to manipulate 'WebClientVariantGroups'."""
    endpoint = "WebClientVariantGroups"
    
    def __init__(self, adapter):
        from ...models._generated._types import WebClientVariantGroup
        self.model = WebClientVariantGroup
        super().__init__(adapter)
