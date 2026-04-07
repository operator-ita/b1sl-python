from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class TaxWebSitesService(GenericResource[Any]):
    endpoint = "TaxWebSitesService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_default_web_site(self, payload: dict | None = None) -> Any:
        """POST TaxWebSitesService_GetDefaultWebSite
        Invoke the method 'GetDefaultWebSite' on this service.
        """
        return self._adapter.post(f"TaxWebSitesService_GetDefaultWebSite", data=payload)

    def get_tax_web_site_list(self, payload: dict | None = None) -> Any:
        """POST TaxWebSitesService_GetTaxWebSiteList
        Invoke the method 'GetTaxWebSiteList' on this service.
        """
        return self._adapter.post(f"TaxWebSitesService_GetTaxWebSiteList", data=payload)
