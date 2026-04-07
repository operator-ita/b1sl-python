from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ProjectManagementService(GenericResource[Any]):
    endpoint = "ProjectManagementService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def add_subproject(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementService_AddSubproject
        Invoke the method 'AddSubproject' on this service by specifying the payload 'PM_SubprojectDocumentData' in the JSON format.

        Example:
        ```json
        {
            "PM_SubprojectDocumentData": {
                "Owner": 2,
                "PMS_StagesCollection": [
                    {
                        "CloseDate": "2016-08-31",
                        "StageType": 7,
                        "StartDate": "2016-08-31"
                    }
                ],
                "ProjectID": "2",
                "StartDate": "2016-08-31",
                "SubprojectEndDate": "2016-08-31",
                "SubprojectName": "subProject1"
            }
        }
        ```
        """
        return self._adapter.post(f"ProjectManagementService_AddSubproject", data=payload)

    def delete_subproject(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementService_DeleteSubproject
        Invoke the method 'DeleteSubproject' on this service by specifying the payload 'PM_SubprojectDocumentParams' in the JSON format.

        Example:
        ```json
        {
            "PM_SubprojectDocumentParams": {
                "AbsEntry": 1
            }
        }
        ```
        """
        return self._adapter.post(f"ProjectManagementService_DeleteSubproject", data=payload)

    def get_subproject(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementService_GetSubproject
        Invoke the method 'GetSubproject' on this service by specifying the payload 'PM_SubprojectDocumentParams' in the JSON format.

        Example:
        ```json
        {
            "PM_SubprojectDocumentParams": {
                "AbsEntry": 1
            }
        }
        ```
        """
        return self._adapter.post(f"ProjectManagementService_GetSubproject", data=payload)

    def get_subprojects_list(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementService_GetSubprojectsList
        Invoke the method 'GetSubprojectsList' on this service by specifying the payload 'PM_SubprojectParams' in the JSON format.

        Example:
        ```json
        {
            "PM_SubprojectParams": {
                "AbsEntry": 2
            }
        }
        ```
        """
        return self._adapter.post(f"ProjectManagementService_GetSubprojectsList", data=payload)

    def update_subproject(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementService_UpdateSubproject
        Invoke the method 'UpdateSubproject' on this service by specifying the payload 'PM_SubprojectDocumentData' in the JSON format.

        Example:
        ```json
        {
            "PM_SubprojectDocumentData": {
                "AbsEntry": 1,
                "ProjectID": "2",
                "StartDate": "2016-08-30",
                "SubprojectName": "new subProject1"
            }
        }
        ```
        """
        return self._adapter.post(f"ProjectManagementService_UpdateSubproject", data=payload)
