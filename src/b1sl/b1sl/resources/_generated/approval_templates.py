from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ApprovalTemplatesService(GenericResource["ApprovalTemplate"]):
    """This entity enables you to manipulate 'ApprovalTemplates'. Each template specifies an approval procedure, and the users and transactions to which the procedure applies."""
    endpoint = "ApprovalTemplates"

    def __init__(self, adapter):
        from ...models._generated._types import ApprovalTemplate
        self.model = ApprovalTemplate
        super().__init__(adapter)
