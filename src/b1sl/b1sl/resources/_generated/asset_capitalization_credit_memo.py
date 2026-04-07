from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class AssetCapitalizationCreditMemoService(GenericResource["AssetDocument"]):
    """This entity enables you to manipulate 'AssetCapitalizationCreditMemo'."""
    endpoint = "AssetCapitalizationCreditMemo"

    def __init__(self, adapter):
        from ...models._generated._types import AssetDocument
        self.model = AssetDocument
        super().__init__(adapter)
