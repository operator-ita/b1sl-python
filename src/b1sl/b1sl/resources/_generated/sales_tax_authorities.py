from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class SalesTaxAuthoritiesService(GenericResource["SalesTaxAuthority"]):
    """This entity enables you to manipulate 'SalesTaxAuthorities'. It represents the sales tax jurisdictions data for the US and Canada localizations, or sales tax types for the Latin America localization."""
    endpoint = "SalesTaxAuthorities"

    def __init__(self, adapter):
        from ...models._generated._types import SalesTaxAuthority
        self.model = SalesTaxAuthority
        super().__init__(adapter)
