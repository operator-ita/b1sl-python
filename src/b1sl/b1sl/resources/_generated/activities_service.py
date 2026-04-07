from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ActivitiesService(GenericResource[Any]):
    endpoint = "ActivitiesService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def delete_single_instance_from_series(self, payload: dict | None = None) -> Any:
        """POST ActivitiesService_DeleteSingleInstanceFromSeries
        Invoke the method 'DeleteSingleInstanceFromSeries' on this service by specifying the payload 'ActivityInstanceParams' in the JSON format.

        Example:
        ```json
        {
            "ActivityInstanceParams": {
                "ActivityCode": "3",
                "InstanceDate": "2016-08-30"
            }
        }
        ```
        """
        return self._adapter.post(f"ActivitiesService_DeleteSingleInstanceFromSeries", data=payload)

    def get_activity_list(self, payload: dict | None = None) -> Any:
        """POST ActivitiesService_GetActivityList
        Invoke the method 'GetActivityList' on this service.
        """
        return self._adapter.post(f"ActivitiesService_GetActivityList", data=payload)

    def get_list_by_attend_user(self, payload: dict | None = None) -> Any:
        """POST ActivitiesService_GetListByAttendUser
        """
        return self._adapter.post(f"ActivitiesService_GetListByAttendUser", data=payload)

    def get_single_instance_from_series(self, payload: dict | None = None) -> Any:
        """POST ActivitiesService_GetSingleInstanceFromSeries
        Invoke the method 'GetSingleInstanceFromSeries' on this service by specifying the payload 'ActivityInstanceParams' in the JSON format.

        Example:
        ```json
        {
            "ActivityInstanceParams": {
                "ActivityCode": "3",
                "InstanceDate": "2016-08-30"
            }
        }
        ```
        """
        return self._adapter.post(f"ActivitiesService_GetSingleInstanceFromSeries", data=payload)

    def get_top_n_activity_instances(self, payload: dict | None = None) -> Any:
        """POST ActivitiesService_GetTopNActivityInstances
        Invoke the method 'GetTopNActivityInstances' on this service by specifying the payload 'ActivityInstancesListParams' in the JSON format.

        Example:
        ```json
        {
            "ActivityInstancesListParams": {
                "ActivityInstancesListParams": {
                    "StartDate": "2016-08-30"
                }
            }
        }
        ```
        """
        return self._adapter.post(f"ActivitiesService_GetTopNActivityInstances", data=payload)

    def init_data(self, payload: dict | None = None) -> Any:
        """POST ActivitiesService_InitData
        """
        return self._adapter.post(f"ActivitiesService_InitData", data=payload)

    def update_single_instance_in_series(self, payload: dict | None = None) -> Any:
        """POST ActivitiesService_UpdateSingleInstanceInSeries
        Invoke the method 'UpdateSingleInstanceInSeries' on this service by specifying the payload 'Activity' in the JSON format.

        Example:
        ```json
        {
            "Activity": {
                "ActivityDate": "2016-08-30",
                "ActivityTime": "08:13:00",
                "CardCode": "C01",
                "DocEntry": "3",
                "DocNum": "1",
                "DocType": "17",
                "Duration": 15,
                "DurationType": "du_Minuts",
                "EndDueDate": "2016-08-30",
                "EndTime": "08:28:00",
                "Reminder": "tYES",
                "ReminderPeriod": 15,
                "ReminderType": "du_Minuts",
                "StartDate": "2016-08-30",
                "StartTime": "08:13:00"
            }
        }
        ```
        """
        return self._adapter.post(f"ActivitiesService_UpdateSingleInstanceInSeries", data=payload)
