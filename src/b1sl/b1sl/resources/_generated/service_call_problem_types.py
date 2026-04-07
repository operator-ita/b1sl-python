from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ServiceCallProblemTypesService(GenericResource["ServiceCallProblemType"]):
    """This entity enables you to manipulate 'ServiceCallProblemTypes'."""
    endpoint = "ServiceCallProblemTypes"
    
    def __init__(self, adapter):
        from ...models._generated._types import ServiceCallProblemType
        self.model = ServiceCallProblemType
        super().__init__(adapter)
