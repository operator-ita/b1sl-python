from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class BlanketAgreementsService(GenericResource[Any]):
    endpoint = "BlanketAgreementsService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_blanket_agreement_list(self, payload: dict | None = None) -> Any:
        """POST BlanketAgreementsService_GetBlanketAgreementList
        Invoke the method 'GetBlanketAgreementList' on this service.
        """
        return self._adapter.post("BlanketAgreementsService_GetBlanketAgreementList", data=payload)
