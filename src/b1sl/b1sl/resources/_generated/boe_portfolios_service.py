from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class BOEPortfoliosService(GenericResource[Any]):
    endpoint = "BOEPortfoliosService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_boe_portfolio_list(self, payload: dict | None = None) -> Any:
        """POST BOEPortfoliosService_GetBOEPortfolioList
        Invoke the method 'GetBOEPortfolioList' on this service.
        """
        return self._adapter.post("BOEPortfoliosService_GetBOEPortfolioList", data=payload)
