from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class BinLocationsService(GenericResource["BinLocation"]):
    """This entity enables you to manipulate 'BinLocations'."""
    endpoint = "BinLocations"

    def __init__(self, adapter):
        from ...models._generated._types import BinLocation
        self.model = BinLocation
        super().__init__(adapter)
