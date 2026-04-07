from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CycleCountDeterminationsService(GenericResource["CycleCountDetermination"]):
    """This entity enables you to manipulate 'CycleCountDeterminations'."""
    endpoint = "CycleCountDeterminations"

    def __init__(self, adapter):
        from ...models._generated._types import CycleCountDetermination
        self.model = CycleCountDetermination
        super().__init__(adapter)
