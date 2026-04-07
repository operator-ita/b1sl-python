from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CurrenciesService(GenericResource["Currency"]):
    """This entity enables you to manipulate 'Currencies'. It represents the currency codes in the Administration module."""
    endpoint = "Currencies"

    def __init__(self, adapter):
        from ...models._generated._types import Currency
        self.model = Currency
        super().__init__(adapter)
