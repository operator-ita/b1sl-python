from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ApprovalRequestsService(GenericResource["ApprovalRequest"]):
    """This entity enables you to manipulate 'ApprovalRequests' and retrieve approval requests for various approval processes."""
    endpoint = "ApprovalRequests"

    def __init__(self, adapter):
        from ...models._generated._types import ApprovalRequest
        self.model = ApprovalRequest
        super().__init__(adapter)
