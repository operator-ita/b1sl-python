from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class DunningLettersService(GenericResource["DunningLetter"]):
    """This entity enables you to manipulate 'DunningLetters'. It represents a list of dunning levels that is used as a template when creating a new dunning term."""
    endpoint = "DunningLetters"

    def __init__(self, adapter):
        from ...models._generated._types import DunningLetter
        self.model = DunningLetter
        super().__init__(adapter)
