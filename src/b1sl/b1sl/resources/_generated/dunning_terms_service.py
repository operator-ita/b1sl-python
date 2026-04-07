from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class DunningTermsService(GenericResource[Any]):
    endpoint = "DunningTermsService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_dunning_term_list(self, payload: dict | None = None) -> Any:
        """POST DunningTermsService_GetDunningTermList
        Invoke the method 'GetDunningTermList' on this service.
        """
        return self._adapter.post(f"DunningTermsService_GetDunningTermList", data=payload)
