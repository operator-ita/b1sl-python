from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class SeriesService(GenericResource[Any]):
    endpoint = "SeriesService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def add_electronic_series(self, payload: dict | None = None) -> Any:
        """POST SeriesService_AddElectronicSeries
        Invoke the method 'AddElectronicSeries' on this service by specifying the payload 'ElectronicSeries' in the JSON format.

        Example:
        ```json
        {
            "ElectronicSeries": {}
        }
        ```
        """
        return self._adapter.post(f"SeriesService_AddElectronicSeries", data=payload)

    def add_series(self, payload: dict | None = None) -> Any:
        """POST SeriesService_AddSeries
        Invoke the method 'AddSeries' on this service by specifying the payload 'Series' in the JSON format.

        Example:
        ```json
        {
            "Series": {
                "ATDocumentType": null,
                "BPLID": null,
                "DigitNumber": 2,
                "Document": "2",
                "DocumentSubType": "C",
                "GroupCode": "sg_Group1",
                "InitialNumber": 21,
                "IsDigitalSeries": "tNO",
                "IsElectronicCommEnabled": "tNO",
                "LastNumber": 30,
                "Locked": "tNO",
                "Name": "New2",
                "NextNumber": 21,
                "PeriodIndicator": "Default",
                "Prefix": "S",
                "Remarks": "test",
                "Series": 70,
                "SeriesType": "stBusinessPartner",
                "Suffix": "b"
            }
        }
        ```
        """
        return self._adapter.post(f"SeriesService_AddSeries", data=payload)

    def attach_series_to_document(self, payload: dict | None = None) -> Any:
        """POST SeriesService_AttachSeriesToDocument
        Invoke the method 'AttachSeriesToDocument' on this service by specifying the payload 'DocumentSeriesParams' in the JSON format.

        Example:
        ```json
        {
            "DocumentSeriesParams": {}
        }
        ```
        """
        return self._adapter.post(f"SeriesService_AttachSeriesToDocument", data=payload)

    def change_document_menu_name(self, payload: dict | None = None) -> Any:
        """POST SeriesService_ChangeDocumentMenuName
        Invoke the method 'ChangeDocumentMenuName' on this service by specifying the payload 'DocumentChangeMenuName' in the JSON format.

        Example:
        ```json
        {
            "DocumentChangeMenuName": {}
        }
        ```
        """
        return self._adapter.post(f"SeriesService_ChangeDocumentMenuName", data=payload)

    def get_default_electronic_series(self, payload: dict | None = None) -> Any:
        """POST SeriesService_GetDefaultElectronicSeries
        Invoke the method 'GetDefaultElectronicSeries' on this service by specifying the payload 'SeriesParams' in the JSON format.

        Example:
        ```json
        {
            "SeriesParams": {}
        }
        ```
        """
        return self._adapter.post(f"SeriesService_GetDefaultElectronicSeries", data=payload)

    def get_default_series(self, payload: dict | None = None) -> Any:
        """POST SeriesService_GetDefaultSeries
        Invoke the method 'GetDefaultSeries' on this service by specifying the payload 'DocumentTypeParams' in the JSON format.

        Example:
        ```json
        {
            "DocumentTypeParams": {}
        }
        ```
        """
        return self._adapter.post(f"SeriesService_GetDefaultSeries", data=payload)

    def get_document_changed_menu_name(self, payload: dict | None = None) -> Any:
        """POST SeriesService_GetDocumentChangedMenuName
        Invoke the method 'GetDocumentChangedMenuName' on this service by specifying the payload 'DocumentTypeParams' in the JSON format.

        Example:
        ```json
        {
            "DocumentTypeParams": {}
        }
        ```
        """
        return self._adapter.post(f"SeriesService_GetDocumentChangedMenuName", data=payload)

    def get_document_series(self, payload: dict | None = None) -> Any:
        """POST SeriesService_GetDocumentSeries
        Invoke the method 'GetDocumentSeries' on this service by specifying the payload 'DocumentTypeParams' in the JSON format.

        Example:
        ```json
        {
            "DocumentTypeParams": {
                "Document": "2",
                "DocumentSubType": "C"
            }
        }
        ```
        """
        return self._adapter.post(f"SeriesService_GetDocumentSeries", data=payload)

    def get_electronic_series(self, payload: dict | None = None) -> Any:
        """POST SeriesService_GetElectronicSeries
        Invoke the method 'GetElectronicSeries' on this service by specifying the payload 'ElectronicSeriesParams' in the JSON format.

        Example:
        ```json
        {
            "ElectronicSeriesParams": {}
        }
        ```
        """
        return self._adapter.post(f"SeriesService_GetElectronicSeries", data=payload)

    def get_series(self, payload: dict | None = None) -> Any:
        """POST SeriesService_GetSeries
        Invoke the method 'GetSeries' on this service by specifying the payload 'SeriesParams' in the JSON format.

        Example:
        ```json
        {
            "SeriesParams": {}
        }
        ```
        """
        return self._adapter.post(f"SeriesService_GetSeries", data=payload)

    def remove_electronic_series(self, payload: dict | None = None) -> Any:
        """POST SeriesService_RemoveElectronicSeries
        Invoke the method 'RemoveElectronicSeries' on this service by specifying the payload 'ElectronicSeriesParams' in the JSON format.

        Example:
        ```json
        {
            "ElectronicSeriesParams": {}
        }
        ```
        """
        return self._adapter.post(f"SeriesService_RemoveElectronicSeries", data=payload)

    def remove_series(self, payload: dict | None = None) -> Any:
        """POST SeriesService_RemoveSeries
        Invoke the method 'RemoveSeries' on this service by specifying the payload 'SeriesParams' in the JSON format.

        Example:
        ```json
        {
            "Series": {
                "ATDocumentType": null,
                "BPLID": null,
                "DigitNumber": 2,
                "Document": "2",
                "DocumentSubType": "C",
                "GroupCode": "sg_Group1",
                "InitialNumber": 21,
                "IsDigitalSeries": "tNO",
                "IsElectronicCommEnabled": "tNO",
                "LastNumber": 30,
                "Locked": "tNO",
                "Name": "New2",
                "NextNumber": 21,
                "PeriodIndicator": "Default",
                "Prefix": "S",
                "Remarks": "test",
                "Series": 70,
                "SeriesType": "stBusinessPartner",
                "Suffix": "b"
            }
        }
        ```
        """
        return self._adapter.post(f"SeriesService_RemoveSeries", data=payload)

    def set_default_electronic_series(self, payload: dict | None = None) -> Any:
        """POST SeriesService_SetDefaultElectronicSeries
        Invoke the method 'SetDefaultElectronicSeries' on this service by specifying the payload 'DefaultElectronicSeriesParams' in the JSON format.

        Example:
        ```json
        {
            "DefaultElectronicSeriesParams": {}
        }
        ```
        """
        return self._adapter.post(f"SeriesService_SetDefaultElectronicSeries", data=payload)

    def set_default_series_for_all_users(self, payload: dict | None = None) -> Any:
        """POST SeriesService_SetDefaultSeriesForAllUsers
        Invoke the method 'SetDefaultSeriesForAllUsers' on this service by specifying the payload 'DocumentSeriesParams' in the JSON format.

        Example:
        ```json
        {
            "DocumentSeriesParams": {}
        }
        ```
        """
        return self._adapter.post(f"SeriesService_SetDefaultSeriesForAllUsers", data=payload)

    def set_default_series_for_current_user(self, payload: dict | None = None) -> Any:
        """POST SeriesService_SetDefaultSeriesForCurrentUser
        Invoke the method 'SetDefaultSeriesForCurrentUser' on this service by specifying the payload 'DocumentSeriesParams' in the JSON format.

        Example:
        ```json
        {
            "DocumentSeriesParams": {}
        }
        ```
        """
        return self._adapter.post(f"SeriesService_SetDefaultSeriesForCurrentUser", data=payload)

    def set_default_series_for_user(self, payload: dict | None = None) -> Any:
        """POST SeriesService_SetDefaultSeriesForUser
        Invoke the method 'SetDefaultSeriesForUser' on this service by specifying the payload 'DocumentSeriesUserParams' in the JSON format.

        Example:
        ```json
        {
            "DocumentSeriesUserParams": {}
        }
        ```
        """
        return self._adapter.post(f"SeriesService_SetDefaultSeriesForUser", data=payload)

    def unattach_series_from_document(self, payload: dict | None = None) -> Any:
        """POST SeriesService_UnattachSeriesFromDocument
        Invoke the method 'UnattachSeriesFromDocument' on this service by specifying the payload 'DocumentSeriesParams' in the JSON format.

        Example:
        ```json
        {
            "DocumentSeriesParams": {}
        }
        ```
        """
        return self._adapter.post(f"SeriesService_UnattachSeriesFromDocument", data=payload)

    def update_electronic_series(self, payload: dict | None = None) -> Any:
        """POST SeriesService_UpdateElectronicSeries
        Invoke the method 'UpdateElectronicSeries' on this service by specifying the payload 'ElectronicSeries' in the JSON format.

        Example:
        ```json
        {
            "ElectronicSeries": {}
        }
        ```
        """
        return self._adapter.post(f"SeriesService_UpdateElectronicSeries", data=payload)

    def update_series(self, payload: dict | None = None) -> Any:
        """POST SeriesService_UpdateSeries
        Invoke the method 'UpdateSeries' on this service by specifying the payload 'Series' in the JSON format.

        Example:
        ```json
        {
            "Series": {}
        }
        ```
        """
        return self._adapter.post(f"SeriesService_UpdateSeries", data=payload)
