from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class FormPreferencesService(GenericResource["ColumnPreferences"]):
    """This entity enables you to manipulate 'FormPreferences'."""
    endpoint = "FormPreferences"

    def __init__(self, adapter):
        from ...models._generated._types import ColumnPreferences
        self.model = ColumnPreferences
        super().__init__(adapter)
