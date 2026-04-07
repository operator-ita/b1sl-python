from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class SalesTaxAuthoritiesTypesService(GenericResource["SalesTaxAuthoritiesType"]):
    """This entity enables you to manipulate 'SalesTaxAuthoritiesTypes'. It represents the types of sales tax authorities. It specifies whether the sales tax authority includes VAT."""
    endpoint = "SalesTaxAuthoritiesTypes"

    def __init__(self, adapter):
        from ...models._generated._types import SalesTaxAuthoritiesType
        self.model = SalesTaxAuthoritiesType
        super().__init__(adapter)
