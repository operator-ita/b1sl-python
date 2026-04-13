from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ResourcesService(GenericResource["Resource"]):
    """This entity enables you to manipulate 'Resources'."""
    endpoint = "Resources"
    
    def __init__(self, adapter):
        from ...models._generated._types import Resource
        self.model = Resource
        super().__init__(adapter)
