from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class OccurrenceCodesService(GenericResource["OccurenceCode"]):
    """This entity enables you to manipulate 'OccurrenceCodes'."""
    endpoint = "OccurrenceCodes"
    
    def __init__(self, adapter):
        from ...models._generated._types import OccurenceCode
        self.model = OccurenceCode
        super().__init__(adapter)
