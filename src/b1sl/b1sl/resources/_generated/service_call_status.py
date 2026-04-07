from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ServiceCallStatusService(GenericResource["ServiceCallStatus"]):
    """This entity enables you to manipulate 'ServiceCallStatus'."""
    endpoint = "ServiceCallStatus"

    def __init__(self, adapter):
        from ...models._generated._types import ServiceCallStatus
        self.model = ServiceCallStatus
        super().__init__(adapter)
