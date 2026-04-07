from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class WeightMeasuresService(GenericResource["WeightMeasure"]):
    """This entity enables you to manipulate 'WeightMeasures'. It defines the weight measure units that are used for item records."""
    endpoint = "WeightMeasures"

    def __init__(self, adapter):
        from ...models._generated._types import WeightMeasure
        self.model = WeightMeasure
        super().__init__(adapter)
