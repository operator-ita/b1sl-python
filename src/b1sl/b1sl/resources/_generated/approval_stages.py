from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ApprovalStagesService(GenericResource["ApprovalStage"]):
    """This entity enables you to manipulate 'ApprovalStages'."""
    endpoint = "ApprovalStages"
    
    def __init__(self, adapter):
        from ...models._generated._types import ApprovalStage
        self.model = ApprovalStage
        super().__init__(adapter)
