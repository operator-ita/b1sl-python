from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ValueMappingCommunicationService(GenericResource["ValueMappingCommunicationData"]):
    """This entity enables you to manipulate 'ValueMappingCommunication'."""
    endpoint = "ValueMappingCommunication"

    def __init__(self, adapter):
        from ...models._generated._types import ValueMappingCommunicationData
        self.model = ValueMappingCommunicationData
        super().__init__(adapter)
