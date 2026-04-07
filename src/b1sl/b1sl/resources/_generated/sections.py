from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class SectionsService(GenericResource["Section"]):
    """This entity enables you to manipulate 'Sections'."""
    endpoint = "Sections"

    def __init__(self, adapter):
        from ...models._generated._types import Section
        self.model = Section
        super().__init__(adapter)
