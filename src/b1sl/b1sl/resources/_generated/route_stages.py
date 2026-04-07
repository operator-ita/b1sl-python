from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class RouteStagesService(GenericResource["RouteStage"]):
    """This entity enables you to manipulate 'RouteStages'."""
    endpoint = "RouteStages"

    def __init__(self, adapter):
        from ...models._generated._types import RouteStage
        self.model = RouteStage
        super().__init__(adapter)
