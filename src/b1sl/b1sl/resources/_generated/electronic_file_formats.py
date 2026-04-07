from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ElectronicFileFormatsService(GenericResource["ElectronicFileFormat"]):
    """This entity enables you to manipulate 'ElectronicFileFormats'. It depends on EFM runtime."""
    endpoint = "ElectronicFileFormats"
    
    def __init__(self, adapter):
        from ...models._generated._types import ElectronicFileFormat
        self.model = ElectronicFileFormat
        super().__init__(adapter)
