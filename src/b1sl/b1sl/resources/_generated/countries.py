from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CountriesService(GenericResource["Country"]):
    """This entity enables you to manipulate 'Countries'. It manages the settings of each country, such as country code, country name and address format."""
    endpoint = "Countries"

    def __init__(self, adapter):
        from ...models._generated._types import Country
        self.model = Country
        super().__init__(adapter)
