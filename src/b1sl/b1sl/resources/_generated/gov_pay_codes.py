from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class GovPayCodesService(GenericResource["GovPayCode"]):
    """This entity enables you to manipulate 'GovPayCodes'."""
    endpoint = "GovPayCodes"
    
    def __init__(self, adapter):
        from ...models._generated._types import GovPayCode
        self.model = GovPayCode
        super().__init__(adapter)
