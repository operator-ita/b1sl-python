from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class MobileAddOnSettingService(GenericResource[Any]):
    endpoint = "MobileAddOnSettingService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_mobile_add_on_setting_list(self, payload: dict | None = None) -> Any:
        """POST MobileAddOnSettingService_GetMobileAddOnSettingList
        Invoke the method 'GetMobileAddOnSettingList' on this service.
        """
        return self._adapter.post("MobileAddOnSettingService_GetMobileAddOnSettingList", data=payload)
