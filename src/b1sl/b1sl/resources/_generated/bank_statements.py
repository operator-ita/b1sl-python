from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class BankStatementsService(GenericResource["BankStatement"]):
    """This entity enables you to manipulate 'BankStatements'."""
    endpoint = "BankStatements"

    def __init__(self, adapter):
        from ...models._generated._types import BankStatement
        self.model = BankStatement
        super().__init__(adapter)
