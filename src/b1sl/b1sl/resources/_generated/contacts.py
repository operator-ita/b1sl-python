from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ContactsService(GenericResource["Contact"]):
    """This entity enables you to manipulate 'Contacts'. It represents the activities carried out with customers and vendors."""
    endpoint = "Contacts"

    def __init__(self, adapter):
        from ...models._generated._types import Contact
        self.model = Contact
        super().__init__(adapter)
