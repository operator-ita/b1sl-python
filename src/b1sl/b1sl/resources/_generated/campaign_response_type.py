from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CampaignResponseTypeService(GenericResource["CampaignResponseType"]):
    """This entity enables you to manipulate 'CampaignResponseType'."""
    endpoint = "CampaignResponseType"
    
    def __init__(self, adapter):
        from ...models._generated._types import CampaignResponseType
        self.model = CampaignResponseType
        super().__init__(adapter)
