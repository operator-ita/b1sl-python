from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class TaxWebSitesService(GenericResource["TaxWebSite"]):
    """This entity enables you to manipulate 'TaxWebSites'."""
    endpoint = "TaxWebSites"

    def __init__(self, adapter):
        from ...models._generated._types import TaxWebSite
        self.model = TaxWebSite
        super().__init__(adapter)
