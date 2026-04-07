from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CountriesService(GenericResource[Any]):
    endpoint = "CountriesService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_country_list(self, payload: dict | None = None) -> Any:
        """POST CountriesService_GetCountryList
        Invoke the method 'GetCountryList' on this service.
        """
        return self._adapter.post("CountriesService_GetCountryList", data=payload)
