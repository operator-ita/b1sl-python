from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class TrackingNotesService(GenericResource["TrackingNote"]):
    """This entity enables you to manipulate 'TrackingNotes'."""
    endpoint = "TrackingNotes"

    def __init__(self, adapter):
        from ...models._generated._types import TrackingNote
        self.model = TrackingNote
        super().__init__(adapter)
