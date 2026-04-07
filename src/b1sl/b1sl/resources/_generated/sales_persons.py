from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class SalesPersonsService(GenericResource["SalesPerson"]):
    """This entity enables you to manipulate 'SalesPersons'. It defines sales employees and their commission rates."""
    endpoint = "SalesPersons"

    def __init__(self, adapter):
        from ...models._generated._types import SalesPerson
        self.model = SalesPerson
        super().__init__(adapter)
