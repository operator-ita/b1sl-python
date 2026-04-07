from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ManufacturersService(GenericResource["Manufacturer"]):
    """This entity enables you to manipulate 'Manufacturers'. It defines manufacturers used in the Item master data."""
    endpoint = "Manufacturers"

    def __init__(self, adapter):
        from ...models._generated._types import Manufacturer
        self.model = Manufacturer
        super().__init__(adapter)
