from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CountiesService(GenericResource["County"]):
    """This entity enables you to manipulate 'Counties'."""
    endpoint = "Counties"
    
    def __init__(self, adapter):
        from ...models._generated._types import County
        self.model = County
        super().__init__(adapter)
