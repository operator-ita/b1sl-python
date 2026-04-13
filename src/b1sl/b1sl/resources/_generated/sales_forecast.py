from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class SalesForecastService(GenericResource["SalesForecast"]):
    """This entity enables you to manipulate 'SalesForecast'. It represents the sales forecast for a specified period."""
    endpoint = "SalesForecast"
    
    def __init__(self, adapter):
        from ...models._generated._types import SalesForecast
        self.model = SalesForecast
        super().__init__(adapter)
