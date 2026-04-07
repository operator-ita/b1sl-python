from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class BrazilFuelIndexersService(GenericResource["BrazilFuelIndexer"]):
    """This entity enables you to manipulate 'BrazilFuelIndexers'."""
    endpoint = "BrazilFuelIndexers"
    
    def __init__(self, adapter):
        from ...models._generated._types import BrazilFuelIndexer
        self.model = BrazilFuelIndexer
        super().__init__(adapter)
