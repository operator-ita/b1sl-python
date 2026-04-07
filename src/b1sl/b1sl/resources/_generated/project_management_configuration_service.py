from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ProjectManagementConfigurationService(GenericResource[Any]):
    endpoint = "ProjectManagementConfigurationService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def add_activities(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementConfigurationService_AddActivities
        Invoke the method 'AddActivities' on this service by specifying the payload 'Collection(PMC_ActivityData)' in the JSON format.

        Example:
        ```json
        {
            "PMC_ActivityData": {
                "ActivityType": "calls",
                "IsChargeable": "tYES"
            }
        }
        ```
        """
        return self._adapter.post("ProjectManagementConfigurationService_AddActivities", data=payload)

    def add_areas(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementConfigurationService_AddAreas
        Invoke the method 'AddAreas' on this service by specifying the payload 'Collection(PMC_AreaData)' in the JSON format.

        Example:
        ```json
        {
            "PMC_AreaData": {
                "AreaName": "area 1"
            }
        }
        ```
        """
        return self._adapter.post("ProjectManagementConfigurationService_AddAreas", data=payload)

    def add_priorities(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementConfigurationService_AddPriorities
        Invoke the method 'AddPriorities' on this service by specifying the payload 'Collection(PMC_PriorityData)' in the JSON format.

        Example:
        ```json
        {
            "PMC_PriorityData": {
                "PriorityName": "Middle level"
            }
        }
        ```
        """
        return self._adapter.post("ProjectManagementConfigurationService_AddPriorities", data=payload)

    def add_stage_types(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementConfigurationService_AddStageTypes
        Invoke the method 'AddStageTypes' on this service by specifying the payload 'Collection(PMC_StageTypeData)' in the JSON format.

        Example:
        ```json
        {
            "PMC_StageTypeData": {
                "StageDescription": "stage 01",
                "StageName": "stage01"
            }
        }
        ```
        """
        return self._adapter.post("ProjectManagementConfigurationService_AddStageTypes", data=payload)

    def add_subproject_types(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementConfigurationService_AddSubprojectTypes
        Invoke the method 'AddSubprojectTypes' on this service by specifying the payload 'Collection(PMC_SubprojectTypeData)' in the JSON format.

        Example:
        ```json
        {
            "PMC_SubprojectTypeData": {
                "SubprojectTypeID": "1",
                "SubprojectTypeName": "subproject 01"
            }
        }
        ```
        """
        return self._adapter.post("ProjectManagementConfigurationService_AddSubprojectTypes", data=payload)

    def add_tasks(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementConfigurationService_AddTasks
        Invoke the method 'AddTasks' on this service by specifying the payload 'Collection(PMC_TaskData)' in the JSON format.

        Example:
        ```json
        {
            "PMC_TaskData": {
                "TaskName": "plans"
            }
        }
        ```
        """
        return self._adapter.post("ProjectManagementConfigurationService_AddTasks", data=payload)

    def delete_activities(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementConfigurationService_DeleteActivities
        Invoke the method 'DeleteActivities' on this service by specifying the payload 'Collection(PMC_ActivityData)' in the JSON format.

        Example:
        ```json
        {
            "PMC_ActivityData": {
                "ActivityID": 1,
                "ActivityType": "calls"
            }
        }
        ```
        """
        return self._adapter.post("ProjectManagementConfigurationService_DeleteActivities", data=payload)

    def delete_areas(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementConfigurationService_DeleteAreas
        Invoke the method 'DeleteAreas' on this service by specifying the payload 'Collection(PMC_AreaData)' in the JSON format.

        Example:
        ```json
        {
            "PMC_AreaData": {
                "AreaID": "1"
            }
        }
        ```
        """
        return self._adapter.post("ProjectManagementConfigurationService_DeleteAreas", data=payload)

    def delete_priorities(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementConfigurationService_DeletePriorities
        Invoke the method 'DeletePriorities' on this service by specifying the payload 'Collection(PMC_PriorityData)' in the JSON format.

        Example:
        ```json
        {
            "PMC_PriorityData": {
                "PriorityID": 1,
                "PriorityName": "Lowest level"
            }
        }
        ```
        """
        return self._adapter.post("ProjectManagementConfigurationService_DeletePriorities", data=payload)

    def delete_stage_types(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementConfigurationService_DeleteStageTypes
        Invoke the method 'DeleteStageTypes' on this service by specifying the payload 'Collection(PMC_StageTypeData)' in the JSON format.

        Example:
        ```json
        {
            "PMC_StageTypeData": {
                "StageID": 6
            }
        }
        ```
        """
        return self._adapter.post("ProjectManagementConfigurationService_DeleteStageTypes", data=payload)

    def delete_subproject_types(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementConfigurationService_DeleteSubprojectTypes
        Invoke the method 'DeleteSubprojectTypes' on this service by specifying the payload 'Collection(PMC_SubprojectTypeData)' in the JSON format.

        Example:
        ```json
        {
            "PMC_SubprojectTypeData": {
                "SubprojectTypeID": "1"
            }
        }
        ```
        """
        return self._adapter.post("ProjectManagementConfigurationService_DeleteSubprojectTypes", data=payload)

    def delete_tasks(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementConfigurationService_DeleteTasks
        Invoke the method 'DeleteTasks' on this service by specifying the payload 'Collection(PMC_TaskData)' in the JSON format.

        Example:
        ```json
        {
            "PMC_TaskData": {
                "TaskID": 2,
                "TaskName": "change plans"
            }
        }
        ```
        """
        return self._adapter.post("ProjectManagementConfigurationService_DeleteTasks", data=payload)

    def get_activities(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementConfigurationService_GetActivities
        Invoke the method 'GetActivities' on this service.
        """
        return self._adapter.post("ProjectManagementConfigurationService_GetActivities", data=payload)

    def get_areas(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementConfigurationService_GetAreas
        Invoke the method 'GetAreas' on this service.
        """
        return self._adapter.post("ProjectManagementConfigurationService_GetAreas", data=payload)

    def get_priorities(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementConfigurationService_GetPriorities
        Invoke the method 'GetPriorities' on this service.
        """
        return self._adapter.post("ProjectManagementConfigurationService_GetPriorities", data=payload)

    def get_stage_types(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementConfigurationService_GetStageTypes
        Invoke the method 'GetStageTypes' on this service.
        """
        return self._adapter.post("ProjectManagementConfigurationService_GetStageTypes", data=payload)

    def get_subproject_types(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementConfigurationService_GetSubprojectTypes
        Invoke the method 'GetSubprojectTypes' on this service.
        """
        return self._adapter.post("ProjectManagementConfigurationService_GetSubprojectTypes", data=payload)

    def get_tasks(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementConfigurationService_GetTasks
        Invoke the method 'GetTasks' on this service.
        """
        return self._adapter.post("ProjectManagementConfigurationService_GetTasks", data=payload)

    def update_activities(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementConfigurationService_UpdateActivities
        Invoke the method 'UpdateActivities' on this service by specifying the payload 'Collection(PMC_ActivityData)' in the JSON format.

        Example:
        ```json
        {
            "PMC_ActivityData": {
                "ActivityID": 1,
                "ActivityType": "email"
            }
        }
        ```
        """
        return self._adapter.post("ProjectManagementConfigurationService_UpdateActivities", data=payload)

    def update_areas(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementConfigurationService_UpdateAreas
        Invoke the method 'UpdateAreas' on this service by specifying the payload 'Collection(PMC_AreaData)' in the JSON format.

        Example:
        ```json
        {
            "PMC_AreaData": {
                "AreaID": "1",
                "AreaName": "update area 1 name"
            }
        }
        ```
        """
        return self._adapter.post("ProjectManagementConfigurationService_UpdateAreas", data=payload)

    def update_priorities(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementConfigurationService_UpdatePriorities
        Invoke the method 'UpdatePriorities' on this service by specifying the payload 'Collection(PMC_PriorityData)' in the JSON format.

        Example:
        ```json
        {
            "PMC_PriorityData": {
                "PriorityID": 1,
                "PriorityName": "Lowest level"
            }
        }
        ```
        """
        return self._adapter.post("ProjectManagementConfigurationService_UpdatePriorities", data=payload)

    def update_stage_types(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementConfigurationService_UpdateStageTypes
        Invoke the method 'UpdateStageTypes' on this service by specifying the payload 'Collection(PMC_StageTypeData)' in the JSON format.

        Example:
        ```json
        {
            "PMC_StageTypeData": {
                "StageDescription": "update stage 01 description",
                "StageID": 6,
                "StageName": "stage01"
            }
        }
        ```
        """
        return self._adapter.post("ProjectManagementConfigurationService_UpdateStageTypes", data=payload)

    def update_subproject_types(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementConfigurationService_UpdateSubprojectTypes
        Invoke the method 'UpdateSubprojectTypes' on this service by specifying the payload 'Collection(PMC_SubprojectTypeData)' in the JSON format.

        Example:
        ```json
        {
            "PMC_SubprojectTypeData": {
                "SubprojectTypeID": "1",
                "SubprojectTypeName": "changed subproject 01 name"
            }
        }
        ```
        """
        return self._adapter.post("ProjectManagementConfigurationService_UpdateSubprojectTypes", data=payload)

    def update_tasks(self, payload: dict | None = None) -> Any:
        """POST ProjectManagementConfigurationService_UpdateTasks
        Invoke the method 'UpdateTasks' on this service by specifying the payload 'Collection(PMC_TaskData)' in the JSON format.

        Example:
        ```json
        {
            "PMC_TaskData": {
                "TaskName": "change plans"
            }
        }
        ```
        """
        return self._adapter.post("ProjectManagementConfigurationService_UpdateTasks", data=payload)
