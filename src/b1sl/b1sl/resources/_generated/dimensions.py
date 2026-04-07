from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class DimensionsService(GenericResource["Dimension"]):
    """This entity enables you to manipulate 'Dimensions'."""
    endpoint = "Dimensions"

    def __init__(self, adapter):
        from ...models._generated._types import Dimension
        self.model = Dimension
        super().__init__(adapter)
