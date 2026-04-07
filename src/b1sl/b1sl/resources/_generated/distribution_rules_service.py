from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class DistributionRulesService(GenericResource[Any]):
    endpoint = "DistributionRulesService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_distribution_rule_list(self, payload: dict | None = None) -> Any:
        """POST DistributionRulesService_GetDistributionRuleList
        Invoke the method 'GetDistributionRuleList' on this service.
        """
        return self._adapter.post("DistributionRulesService_GetDistributionRuleList", data=payload)
