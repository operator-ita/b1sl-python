from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class QRCodeService(GenericResource[Any]):
    endpoint = "QRCodeService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def add_or_update_qr_code(self, payload: dict | None = None) -> Any:
        """POST QRCodeService_AddOrUpdateQRCode
        Invoke the method 'AddOrUpdateQRCode' on this service.

        Example:
        ```json
        {
            "QRCodeData": {
                "FieldName": "QRCodeSrc",
                "ObjectAbsEntry": "1",
                "ObjectType": "22",
                "QRCodeText": "This is QR code text."
            }
        }
        ```
        """
        return self._adapter.post("QRCodeService_AddOrUpdateQRCode", data=payload)
