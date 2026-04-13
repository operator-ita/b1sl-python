from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ContractTemplatesService(GenericResource["ContractTemplate"]):
    """This entity enables you to manipulate 'ContractTemplates'."""
    endpoint = "ContractTemplates"
    
    def __init__(self, adapter):
        from ...models._generated._types import ContractTemplate
        self.model = ContractTemplate
        super().__init__(adapter)
