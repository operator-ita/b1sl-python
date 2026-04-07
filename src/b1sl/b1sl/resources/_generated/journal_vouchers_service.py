from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class JournalVouchersService(GenericResource[Any]):
    endpoint = "JournalVouchersService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def add(self, payload: dict | None = None) -> Any:
        """POST JournalVouchersService_Add
        Invoke the method 'Add' on this service by specifying the payload 'Collection(JournalEntry)' in the JSON format.

        Example:
        ```json
        {
            "JournalVoucher": {
                "JournalEntry": {
                    "DueDate": "2014-12-06",
                    "JournalEntryLines": [
                        {
                            "AccountCode": "_SYS00000000094",
                            "Credit": "0",
                            "Debit": "123"
                        },
                        {
                            "AccountCode": "_SYS00000000019",
                            "Credit": "123",
                            "Debit": "0"
                        }
                    ],
                    "ReferenceDate": "2014-12-06"
                }
            }
        }
        ```
        """
        return self._adapter.post(f"JournalVouchersService_Add", data=payload)
