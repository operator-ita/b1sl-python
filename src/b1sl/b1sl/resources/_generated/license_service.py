from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class LicenseService(GenericResource[Any]):
    endpoint = "LicenseService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Functions ---

    def get_installation_number(self, params: dict | None = None) -> Any:
        """POST LicenseService_GetInstallationNumber(params)
        Invoke the method 'GetInstallationNumber' on this service.
        """
        return self._function("LicenseService_GetInstallationNumber", params)
