from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ValueMappingService(GenericResource[Any]):
    endpoint = "ValueMappingService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_mapped_b1_value(self, payload: dict | None = None) -> Any:
        """POST ValueMappingService_GetMappedB1Value
        Invoke the method 'GetMappedB1Value' on this service by specifying the payload 'VM_B1ValuesData' in the JSON format.
				Retreives value from Business One universe, that is mapped to specific 3th party value.

        Example:
        ```json
        {
            "ObjectId": 37,
            "VM_ThirdPartyValuesData": {
                "ThirdPartySystemId": 1,
                "ThirdPartyValue": "AED"
            }
        }
        ```
        """
        return self._adapter.post(f"ValueMappingService_GetMappedB1Value", data=payload)

    def get_third_party_values_for_b1_value(self, payload: dict | None = None) -> Any:
        """POST ValueMappingService_GetThirdPartyValuesForB1Value
        Invoke the method 'GetThirdPartyValuesForB1Value' on this service by specifying the payload 'VM_B1ValuesData' in the JSON format.
				Retrieves all 3th party values for the specific value from Business One universe.

        Example:
        ```json
        {
            "ObjectAbsEntry": "CHF",
            "ObjectId": 37
        }
        ```
        """
        return self._adapter.post(f"ValueMappingService_GetThirdPartyValuesForB1Value", data=payload)

    def remove_mapped_value(self, payload: dict | None = None) -> Any:
        """POST ValueMappingService_RemoveMappedValue
        Invoke the method 'RemoveMappedValue' on this service by specifying the payload 'VM_ThirdPartyValuesData' in the JSON format.
				Removes one 3th party value from the collection of mapped values to one specific value from Business One universe.

        Example:
        ```json
        {
            "AbsEntry": 6,
            "LineId": 2,
            "ThirdPartySystemId": 1
        }
        ```
        """
        return self._adapter.post(f"ValueMappingService_RemoveMappedValue", data=payload)
