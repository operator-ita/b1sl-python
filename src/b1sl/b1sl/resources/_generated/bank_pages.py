from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class BankPagesService(GenericResource["BankPage"]):
    """This entity enables you to manipulate 'BankPages'. It represents external bank statements in the Banking module."""
    endpoint = "BankPages"

    def __init__(self, adapter):
        from ...models._generated._types import BankPage
        self.model = BankPage
        super().__init__(adapter)
