from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class BOEPortfoliosService(GenericResource["BOEPortfolio"]):
    """This entity enables you to manipulate 'BOEPortfolios'."""
    endpoint = "BOEPortfolios"

    def __init__(self, adapter):
        from ...models._generated._types import BOEPortfolio
        self.model = BOEPortfolio
        super().__init__(adapter)
