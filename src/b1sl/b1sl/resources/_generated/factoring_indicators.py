from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class FactoringIndicatorsService(GenericResource["FactoringIndicator"]):
    """This entity enables you to manipulate 'FactoringIndicators'. It defines keys that can be recorded in certain journal entries and used as selection criteria in various reports."""
    endpoint = "FactoringIndicators"

    def __init__(self, adapter):
        from ...models._generated._types import FactoringIndicator
        self.model = FactoringIndicator
        super().__init__(adapter)
