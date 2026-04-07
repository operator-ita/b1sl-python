from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class SerialNumberDetailsService(GenericResource["SerialNumberDetail"]):
    """This entity enables you to manipulate 'SerialNumberDetails'."""
    endpoint = "SerialNumberDetails"
    
    def __init__(self, adapter):
        from ...models._generated._types import SerialNumberDetail
        self.model = SerialNumberDetail
        super().__init__(adapter)
