from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class PaymentCalculationService(GenericResource[Any]):
    endpoint = "PaymentCalculationService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_payment_amount(self, payload: dict | None = None) -> Any:
        """POST PaymentCalculationService_GetPaymentAmount
        Invoke the method 'GetPaymentAmount' on this service by specifying the payload 'PaymentBPCode,PaymentInvoiceEntries' in the JSON format.

        Example:
        ```json
        {
            "PaymentBPCode": {
                "BPCode": "C01",
                "Date": "2016-08-30"
            },
            "PaymentInvoiceEntries": [
                {
                    "DocEntry": "12",
                    "DocType": "itARInvoice"
                }
            ]
        }
        ```
        """
        return self._adapter.post("PaymentCalculationService_GetPaymentAmount", data=payload)
