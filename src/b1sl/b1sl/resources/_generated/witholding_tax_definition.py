from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class WitholdingTaxDefinitionService(GenericResource["WTDCode"]):
    """This entity enables you to manipulate 'WitholdingTaxDefinition'. It functionally overlaps `WithholdingTaxCodes`."""
    endpoint = "WitholdingTaxDefinition"

    def __init__(self, adapter):
        from ...models._generated._types import WTDCode
        self.model = WTDCode
        super().__init__(adapter)
