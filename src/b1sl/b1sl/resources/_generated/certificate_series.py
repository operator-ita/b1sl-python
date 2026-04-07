from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CertificateSeriesService(GenericResource["CertificateSeries"]):
    """This entity enables you to manipulate 'CertificateSeries'."""
    endpoint = "CertificateSeries"
    
    def __init__(self, adapter):
        from ...models._generated._types import CertificateSeries
        self.model = CertificateSeries
        super().__init__(adapter)
