from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class UserMenuService(GenericResource[Any]):
    endpoint = "UserMenuService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_user_menu(self, payload: dict | None = None) -> Any:
        """POST UserMenuService_GetUserMenu
        Invoke the method 'GetUserMenu' on this service by specifying the payload 'UserMenuParams' in the JSON format.

        Example:
        ```json
        {
            "UserMenuParams": {}
        }
        ```
        """
        return self._adapter.post("UserMenuService_GetUserMenu", data=payload)

    def update_current_user_menu(self, payload: dict | None = None) -> Any:
        """POST UserMenuService_UpdateCurrentUserMenu
        Invoke the method 'UpdateCurrentUserMenu' on this service by specifying the payload 'Collection(UserMenuItem)' in the JSON format.

        Example:
        ```json
        {
            "UserMenuItems": [
                {
                    "LinkedFormMenuID": "11",
                    "LinkedFormNum": null,
                    "LinkedObjKey": null,
                    "LinkedObjType": null,
                    "Name": "Forms",
                    "Position": 1,
                    "ReportPath": "11",
                    "Type": "umitFolder"
                },
                {
                    "LinkedFormMenuID": null,
                    "LinkedFormNum": null,
                    "LinkedObjKey": null,
                    "LinkedObjType": null,
                    "Name": "Reports",
                    "Position": 2,
                    "ReportPath": "",
                    "Type": "umitFolder"
                },
                {
                    "LinkedFormMenuID": null,
                    "LinkedFormNum": null,
                    "LinkedObjKey": null,
                    "LinkedObjType": null,
                    "Name": "Queries",
                    "Position": 3,
                    "ReportPath": "",
                    "Type": "umitFolder"
                },
                {
                    "LinkedFormMenuID": null,
                    "LinkedFormNum": null,
                    "LinkedObjKey": null,
                    "LinkedObjType": null,
                    "Name": "Links",
                    "Position": 4,
                    "ReportPath": "",
                    "Type": "umitFolder"
                }
            ]
        }
        ```
        """
        return self._adapter.post("UserMenuService_UpdateCurrentUserMenu", data=payload)

    def update_user_menu(self, payload: dict | None = None) -> Any:
        """POST UserMenuService_UpdateUserMenu
        Invoke the method 'UpdateUserMenu' on this service by specifying the payload 'UserMenuParams' in the JSON format.

        Example:
        ```json
        {
            "UserMenuParams": {}
        }
        ```
        """
        return self._adapter.post("UserMenuService_UpdateUserMenu", data=payload)

    # --- Functions ---

    def get_current_user_menu(self, params: dict | None = None) -> Any:
        """POST UserMenuService_GetCurrentUserMenu(params)
        Invoke the method 'GetCurrentUserMenu' on this service.
        """
        return self._function("UserMenuService_GetCurrentUserMenu", params)
