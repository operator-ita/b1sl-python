from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ValueMappingService(GenericResource["VM_B1ValuesData"]):
    """This entity enables you to manipulate 'ValueMapping'."""
    endpoint = "ValueMapping"

    def __init__(self, adapter):
        from ...models._generated._types import VM_B1ValuesData
        self.model = VM_B1ValuesData
        super().__init__(adapter)
