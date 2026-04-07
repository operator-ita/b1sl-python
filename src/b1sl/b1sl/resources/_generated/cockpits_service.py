from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CockpitsService(GenericResource[Any]):
    endpoint = "CockpitsService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_cockpit_list(self, payload: dict | None = None) -> Any:
        """POST CockpitsService_GetCockpitList
        Invoke the method 'GetCockpitList' on this service.
        """
        return self._adapter.post(f"CockpitsService_GetCockpitList", data=payload)

    def get_template_cockpit_list(self, payload: dict | None = None) -> Any:
        """POST CockpitsService_GetTemplateCockpitList
        Invoke the method 'GetTemplateCockpitList' on this service.
        """
        return self._adapter.post(f"CockpitsService_GetTemplateCockpitList", data=payload)

    def get_user_cockpit_list(self, payload: dict | None = None) -> Any:
        """POST CockpitsService_GetUserCockpitList
        Invoke the method 'GetUserCockpitList' on this service.
        """
        return self._adapter.post(f"CockpitsService_GetUserCockpitList", data=payload)

    def publish_cockpit(self, payload: dict | None = None) -> Any:
        """POST CockpitsService_PublishCockpit
        Invoke the method 'PublishCockpit' on this service by specifying the payload 'Cockpit' in the JSON format.

        Example:
        ```json
        {
            "Cockpit": {}
        }
        ```
        """
        return self._adapter.post(f"CockpitsService_PublishCockpit", data=payload)
