from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class LengthMeasuresService(GenericResource["LengthMeasure"]):
    """This entity enables you to manipulate 'LengthMeasures'. It defines the length and width measure units that are used for item records."""
    endpoint = "LengthMeasures"

    def __init__(self, adapter):
        from ...models._generated._types import LengthMeasure
        self.model = LengthMeasure
        super().__init__(adapter)
