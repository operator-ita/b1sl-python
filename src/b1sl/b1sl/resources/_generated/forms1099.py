from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class Forms1099Service(GenericResource["Forms1099"]):
    """This entity enables you to manipulate 'Forms1099'. It defines new Form 1099 types in addition to the existing types: 1099 Miscellaneous, 1099 Interest, and 1099 Dividends."""
    endpoint = "Forms1099"
    
    def __init__(self, adapter):
        from ...models._generated._types import Forms1099
        self.model = Forms1099
        super().__init__(adapter)
