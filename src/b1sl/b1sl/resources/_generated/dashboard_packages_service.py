from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class DashboardPackagesService(GenericResource[Any]):
    endpoint = "DashboardPackagesService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def import_dashboard_package(self, payload: dict | None = None) -> Any:
        """POST DashboardPackagesService_ImportDashboardPackage
        Invoke the method 'ImportDashboardPackage' on this service by specifying the payload 'DashboardPackageImportParams' in the JSON format.

        Example:
        ```json
        {
            "DashboardPackageImportParams": {}
        }
        ```
        """
        return self._adapter.post("DashboardPackagesService_ImportDashboardPackage", data=payload)
