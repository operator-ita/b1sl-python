from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class DynamicSystemStringsService(GenericResource["DynamicSystemString"]):
    """This entity enables you to manipulate 'DynamicSystemStrings' and enables modifying a field name and format in the interface to match the terms used in your company."""
    endpoint = "DynamicSystemStrings"

    def __init__(self, adapter):
        from ...models._generated._types import DynamicSystemString
        self.model = DynamicSystemString
        super().__init__(adapter)
