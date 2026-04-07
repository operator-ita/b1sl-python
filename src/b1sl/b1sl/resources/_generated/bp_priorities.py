from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class BPPrioritiesService(GenericResource["BPPriority"]):
    """This entity enables you to manipulate 'BPPriorities'."""
    endpoint = "BPPriorities"
    
    def __init__(self, adapter):
        from ...models._generated._types import BPPriority
        self.model = BPPriority
        super().__init__(adapter)
