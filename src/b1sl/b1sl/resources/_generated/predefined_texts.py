from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class PredefinedTextsService(GenericResource["PredefinedText"]):
    """This entity enables you to manipulate 'PredefinedTexts'."""
    endpoint = "PredefinedTexts"

    def __init__(self, adapter):
        from ...models._generated._types import PredefinedText
        self.model = PredefinedText
        super().__init__(adapter)
