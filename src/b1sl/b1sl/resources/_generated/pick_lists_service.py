from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class PickListsService(GenericResource[Any]):
    endpoint = "PickListsService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def close(self, payload: dict | None = None) -> Any:
        """POST PickListsService_Close
        Invoke the method 'Close' on this service by specifying the payload 'PickList' in the JSON format.

        Example:
        ```json
        {
            "PickList": {
                "Absoluteentry": 3
            }
        }
        ```
        """
        return self._adapter.post("PickListsService_Close", data=payload)

    def update_released_allocation(self, payload: dict | None = None) -> Any:
        """POST PickListsService_UpdateReleasedAllocation
        Invoke the method 'UpdateReleasedAllocation' on this service by specifying the payload 'PickList' in the JSON format.

        Example:
        ```json
        {
            "PickList": {
                "Absoluteentry": 3,
                "Name": "manager",
                "ObjectType": "156",
                "OwnerCode": 1,
                "PickDate": "2016-08-25",
                "PickListsLines": [
                    {
                        "AbsoluteEntry": 3,
                        "BaseObjectType": 17,
                        "DocumentLinesBinAllocations": [
                            {
                                "BinAbsEntry": 2,
                                "Quantity": 1,
                                "SerialAndBatchNumbersBaseLine": 0
                            }
                        ],
                        "LineNumber": 0,
                        "OrderEntry": 9,
                        "OrderRowID": 0,
                        "PickStatus": "ps_Released",
                        "PickedQuantity": 0,
                        "PreviouslyReleasedQuantity": 1,
                        "ReleasedQuantity": 1,
                        "SerialNumbers": [
                            {
                                "InternalSerialNumber": 4,
                                "ManufacturerSerialNumber": 4,
                                "Quantity": 1
                            }
                        ]
                    }
                ],
                "Status": "ps_Released",
                "UseBaseUnits": "tNO"
            }
        }
        ```
        """
        return self._adapter.post("PickListsService_UpdateReleasedAllocation", data=payload)
