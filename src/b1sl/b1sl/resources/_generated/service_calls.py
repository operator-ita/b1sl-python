from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ServiceCallsService(GenericResource["ServiceCall"]):
    """This entity enables you to manipulate 'ServiceCalls'. It represents the service calls in the Service module. Service calls are used to manage service and support activities that you provide to your customers."""
    endpoint = "ServiceCalls"

    def __init__(self, adapter):
        from ...models._generated._types import ServiceCall
        self.model = ServiceCall
        super().__init__(adapter)
