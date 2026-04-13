from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class NCMCodesSetupService(GenericResource["NCMCodeSetup"]):
    """This entity enables you to manipulate 'NCMCodesSetup'."""
    endpoint = "NCMCodesSetup"
    
    def __init__(self, adapter):
        from ...models._generated._types import NCMCodeSetup
        self.model = NCMCodeSetup
        super().__init__(adapter)
