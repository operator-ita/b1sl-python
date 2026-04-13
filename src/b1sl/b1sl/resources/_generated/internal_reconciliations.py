from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class InternalReconciliationsService(GenericResource["InternalReconciliation"]):
    """This entity enables you to manipulate 'InternalReconciliations'."""
    endpoint = "InternalReconciliations"
    
    def __init__(self, adapter):
        from ...models._generated._types import InternalReconciliation
        self.model = InternalReconciliation
        super().__init__(adapter)
