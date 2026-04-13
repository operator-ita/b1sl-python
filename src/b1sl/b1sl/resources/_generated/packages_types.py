from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class PackagesTypesService(GenericResource["PackagesType"]):
    """This entity enables you to manipulate 'PackagesTypes'. It represents various packaging types for deliveries."""
    endpoint = "PackagesTypes"
    
    def __init__(self, adapter):
        from ...models._generated._types import PackagesType
        self.model = PackagesType
        super().__init__(adapter)
