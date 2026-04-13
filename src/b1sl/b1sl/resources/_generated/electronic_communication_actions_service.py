from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ElectronicCommunicationActionsService(GenericResource[Any]):
    endpoint = "ElectronicCommunicationActionsService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def add_ecm_action(self, payload: dict | None = None) -> Any:
        """POST ElectronicCommunicationActionsService_AddEcmAction
        Invoke the method 'AddEcmAction' on this service by specifying the payload 'EcmAction' in the JSON format.

        Example:
        ```json
        {
            "EcmAction": {}
        }
        ```
        """
        return self._adapter.post(f"ElectronicCommunicationActionsService_AddEcmAction", data=payload)

    def add_ecm_action_log(self, payload: dict | None = None) -> Any:
        """POST ElectronicCommunicationActionsService_AddEcmActionLog
        Invoke the method 'AddEcmActionLog' on this service by specifying the payload 'EcmActionLog' in the JSON format.

        Example:
        ```json
        {
            "EcmActionLog": {}
        }
        ```
        """
        return self._adapter.post(f"ElectronicCommunicationActionsService_AddEcmActionLog", data=payload)

    def delete_ecm_action(self, payload: dict | None = None) -> Any:
        """POST ElectronicCommunicationActionsService_DeleteEcmAction
        Invoke the method 'DeleteEcmAction' on this service by specifying the payload 'EcmAction' in the JSON format.

        Example:
        ```json
        {
            "EcmAction": {}
        }
        ```
        """
        return self._adapter.post(f"ElectronicCommunicationActionsService_DeleteEcmAction", data=payload)

    def get_ecm_action(self, payload: dict | None = None) -> Any:
        """POST ElectronicCommunicationActionsService_GetEcmAction
        Invoke the method 'GetEcmAction' on this service by specifying the payload 'EcmActionParams' in the JSON format.

        Example:
        ```json
        {
            "EcmActionParams": {}
        }
        ```
        """
        return self._adapter.post(f"ElectronicCommunicationActionsService_GetEcmAction", data=payload)

    def get_ecm_action_by_doc(self, payload: dict | None = None) -> Any:
        """POST ElectronicCommunicationActionsService_GetEcmActionByDoc
        Invoke the method 'GetEcmActionByDoc' on this service by specifying the payload 'EcmActionDocParams' in the JSON format.

        Example:
        ```json
        {
            "EcmActionDocParams": {}
        }
        ```
        """
        return self._adapter.post(f"ElectronicCommunicationActionsService_GetEcmActionByDoc", data=payload)

    def get_ecm_action_log(self, payload: dict | None = None) -> Any:
        """POST ElectronicCommunicationActionsService_GetEcmActionLog
        Invoke the method 'GetEcmActionLog' on this service by specifying the payload 'EcmActionLogParams' in the JSON format.

        Example:
        ```json
        {
            "EcmActionLogParams": {}
        }
        ```
        """
        return self._adapter.post(f"ElectronicCommunicationActionsService_GetEcmActionLog", data=payload)

    def get_ecm_action_log_list(self, payload: dict | None = None) -> Any:
        """POST ElectronicCommunicationActionsService_GetEcmActionLogList
        Invoke the method 'GetEcmActionLogList' on this service by specifying the payload 'EcmAction' in the JSON format.

        Example:
        ```json
        {
            "EcmAction": {}
        }
        ```
        """
        return self._adapter.post(f"ElectronicCommunicationActionsService_GetEcmActionLogList", data=payload)

    def update_ecm_action(self, payload: dict | None = None) -> Any:
        """POST ElectronicCommunicationActionsService_UpdateEcmAction
        Invoke the method 'UpdateEcmAction' on this service by specifying the payload 'EcmAction' in the JSON format.

        Example:
        ```json
        {
            "EcmAction": {}
        }
        ```
        """
        return self._adapter.post(f"ElectronicCommunicationActionsService_UpdateEcmAction", data=payload)
