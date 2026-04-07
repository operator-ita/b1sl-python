from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class JournalEntryDocumentTypesService(GenericResource["JournalEntryDocumentType"]):
    """This entity enables you to manipulate 'JournalEntryDocumentTypes'."""
    endpoint = "JournalEntryDocumentTypes"

    def __init__(self, adapter):
        from ...models._generated._types import JournalEntryDocumentType
        self.model = JournalEntryDocumentType
        super().__init__(adapter)
