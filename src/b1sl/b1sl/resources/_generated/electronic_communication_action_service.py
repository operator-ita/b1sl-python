from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ElectronicCommunicationActionService(GenericResource[Any]):
    endpoint = "ElectronicCommunicationActionService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def afe_fce_ap_check_ecm2_entry(self, payload: dict | None = None) -> Any:
        """POST ElectronicCommunicationActionService_AFE_FceAP_CheckECM2Entry
        """
        return self._adapter.post(f"ElectronicCommunicationActionService_AFE_FceAP_CheckECM2Entry", data=payload)

    def afe_fce_action_get_by_fce_id(self, payload: dict | None = None) -> Any:
        """POST ElectronicCommunicationActionService_AFE_FceAction_GetByFceID
        """
        return self._adapter.post(f"ElectronicCommunicationActionService_AFE_FceAction_GetByFceID", data=payload)

    def afe_fce_action_get_payment_data(self, payload: dict | None = None) -> Any:
        """POST ElectronicCommunicationActionService_AFE_FceAction_GetPaymentData
        """
        return self._adapter.post(f"ElectronicCommunicationActionService_AFE_FceAction_GetPaymentData", data=payload)

    def afe_renumber_folio_numbers(self, payload: dict | None = None) -> Any:
        """POST ElectronicCommunicationActionService_AFE_RenumberFolioNumbers
        """
        return self._adapter.post(f"ElectronicCommunicationActionService_AFE_RenumberFolioNumbers", data=payload)

    def confirm_success_of_communication(self, payload: dict | None = None) -> Any:
        """POST ElectronicCommunicationActionService_ConfirmSuccessOfCommunication
        Invoke the method 'ConfirmSuccessOfCommunication' on this service by specifying the payload 'ECMCodeParams' in the JSON format.

        Example:
        ```json
        {
            "ECMCodeParams": {}
        }
        ```
        """
        return self._adapter.post(f"ElectronicCommunicationActionService_ConfirmSuccessOfCommunication", data=payload)

    def get_action(self, payload: dict | None = None) -> Any:
        """POST ElectronicCommunicationActionService_GetAction
        Invoke the method 'GetAction' on this service by specifying the payload 'ECMCodeParams' in the JSON format.

        Example:
        ```json
        {
            "ECMCodeParams": {}
        }
        ```
        """
        return self._adapter.post(f"ElectronicCommunicationActionService_GetAction", data=payload)

    def report_error_and_continue(self, payload: dict | None = None) -> Any:
        """POST ElectronicCommunicationActionService_ReportErrorAndContinue
        Invoke the method 'ReportErrorAndContinue' on this service by specifying the payload 'ECMCodeParams' in the JSON format.

        Example:
        ```json
        {
            "ECMCodeParams": {}
        }
        ```
        """
        return self._adapter.post(f"ElectronicCommunicationActionService_ReportErrorAndContinue", data=payload)

    def report_error_and_stop(self, payload: dict | None = None) -> Any:
        """POST ElectronicCommunicationActionService_ReportErrorAndStop
        Invoke the method 'ReportErrorAndStop' on this service by specifying the payload 'ECMCodeParams' in the JSON format.

        Example:
        ```json
        {
            "ECMCodeParams": {}
        }
        ```
        """
        return self._adapter.post(f"ElectronicCommunicationActionService_ReportErrorAndStop", data=payload)

    def update_action(self, payload: dict | None = None) -> Any:
        """POST ElectronicCommunicationActionService_UpdateAction
        Invoke the method 'UpdateAction' on this service by specifying the payload 'ECMActionStatusData' in the JSON format.

        Example:
        ```json
        {
            "ECMActionStatusData": {}
        }
        ```
        """
        return self._adapter.post(f"ElectronicCommunicationActionService_UpdateAction", data=payload)

    # --- Functions ---

    def afe_fce_ap_get_latest_afip_date(self, params: dict | None = None) -> Any:
        """GET ElectronicCommunicationActionService_AFE_FceAP_GetLatestAFIPDate(params)
        """
        return self._function(f"ElectronicCommunicationActionService_AFE_FceAP_GetLatestAFIPDate", params)

    def afe_fce_ar_get_date_from_to(self, params: dict | None = None) -> Any:
        """GET ElectronicCommunicationActionService_AFE_FceAR_GetDateFromTo(params)
        """
        return self._function(f"ElectronicCommunicationActionService_AFE_FceAR_GetDateFromTo", params)

    def afe_fce_ar_get_documents(self, params: dict | None = None) -> Any:
        """GET ElectronicCommunicationActionService_AFE_FceAR_GetDocuments(params)
        """
        return self._function(f"ElectronicCommunicationActionService_AFE_FceAR_GetDocuments", params)

    def afe_upd_fce_apar_get_documents(self, params: dict | None = None) -> Any:
        """GET ElectronicCommunicationActionService_AFE_UpdFceAPAR_GetDocuments(params)
        """
        return self._function(f"ElectronicCommunicationActionService_AFE_UpdFceAPAR_GetDocuments", params)
