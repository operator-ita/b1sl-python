from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class AlternateCatNumService(GenericResource["AlternateCatNum"]):
    """This entity enables you to manipulate 'AlternateCatNum'. It represents the alternative catalog numbers in the Business Partners module."""
    endpoint = "AlternateCatNum"

    def __init__(self, adapter):
        from ...models._generated._types import AlternateCatNum
        self.model = AlternateCatNum
        super().__init__(adapter)
