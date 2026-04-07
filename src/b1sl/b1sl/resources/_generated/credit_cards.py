from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CreditCardsService(GenericResource["CreditCard"]):
    """This entity enables you to manipulate 'CreditCards'. It defines credit cards that the company can use for incoming and outgoing payments."""
    endpoint = "CreditCards"

    def __init__(self, adapter):
        from ...models._generated._types import CreditCard
        self.model = CreditCard
        super().__init__(adapter)
