from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class WorkflowTaskService(GenericResource[Any]):
    endpoint = "WorkflowTaskService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def complete(self, payload: dict | None = None) -> Any:
        """POST WorkflowTaskService_Complete
        Invoke the method 'Complete' on this service by specifying the payload 'WorkflowTaskCompleteParams' in the JSON format.

        Example:
        ```json
        {
            "WorkflowTaskCompleteParams": {
                "Note": "Default Comment",
                "TaskID": "4",
                "TriggerParams": "<Params><Param><Key>Result</Key><Value Type="string">1</Value></Param></Params>"
            }
        }
        ```
        """
        return self._adapter.post(f"WorkflowTaskService_Complete", data=payload)

    def get_approval_task_list(self, payload: dict | None = None) -> Any:
        """POST WorkflowTaskService_GetApprovalTaskList
        Invoke the method 'GetApprovalTaskList' on this service by specifying the payload 'WorkflowApprovalTaskListParams' in the JSON format.

        Example:
        ```json
        {
            "WorkflowApprovalTaskListParams": {
                "Status": "G|W"
            }
        }
        ```
        """
        return self._adapter.post(f"WorkflowTaskService_GetApprovalTaskList", data=payload)
