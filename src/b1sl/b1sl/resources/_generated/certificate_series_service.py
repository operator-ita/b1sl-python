from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CertificateSeriesService(GenericResource[Any]):
    endpoint = "CertificateSeriesService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_certificate_series_list(self, payload: dict | None = None) -> Any:
        """POST CertificateSeriesService_GetCertificateSeriesList
        Invoke the method 'GetCertificateSeriesList' on this service.
        """
        return self._adapter.post("CertificateSeriesService_GetCertificateSeriesList", data=payload)
