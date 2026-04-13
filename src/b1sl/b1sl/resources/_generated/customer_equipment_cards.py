from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CustomerEquipmentCardsService(GenericResource["CustomerEquipmentCard"]):
    """This entity enables you to manipulate 'CustomerEquipmentCards'. It represents the customer equipment cards. For each item sold and managed by a serial number, you can create a customer equipment card to track the after-sales services provided for this item."""
    endpoint = "CustomerEquipmentCards"
    
    def __init__(self, adapter):
        from ...models._generated._types import CustomerEquipmentCard
        self.model = CustomerEquipmentCard
        super().__init__(adapter)
