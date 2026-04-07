from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class JournalEntriesService(GenericResource["JournalEntry"]):
    """This entity enables you to manipulate 'JournalEntries'. It represents journal transactions."""
    endpoint = "JournalEntries"

    def __init__(self, adapter):
        from ...models._generated._types import JournalEntry
        self.model = JournalEntry
        super().__init__(adapter)
