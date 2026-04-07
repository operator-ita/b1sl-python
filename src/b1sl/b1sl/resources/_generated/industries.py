from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class IndustriesService(GenericResource["Industry"]):
    """This entity enables you to manipulate 'Industries'. It represents the industries list from which an industry can be associated with a sales opportunity."""
    endpoint = "Industries"

    def __init__(self, adapter):
        from ...models._generated._types import Industry
        self.model = Industry
        super().__init__(adapter)
