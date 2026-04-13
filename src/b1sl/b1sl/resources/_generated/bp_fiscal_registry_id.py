from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class BPFiscalRegistryIDService(GenericResource["BPFiscalRegistryID"]):
    """This entity enables you to manipulate 'BPFiscalRegistryID'."""
    endpoint = "BPFiscalRegistryID"
    
    def __init__(self, adapter):
        from ...models._generated._types import BPFiscalRegistryID
        self.model = BPFiscalRegistryID
        super().__init__(adapter)
