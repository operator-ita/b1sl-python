from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ServiceCallProblemSubTypesService(GenericResource["ServiceCallProblemSubType"]):
    """This entity enables you to manipulate 'ServiceCallProblemSubTypes'."""
    endpoint = "ServiceCallProblemSubTypes"
    
    def __init__(self, adapter):
        from ...models._generated._types import ServiceCallProblemSubType
        self.model = ServiceCallProblemSubType
        super().__init__(adapter)
