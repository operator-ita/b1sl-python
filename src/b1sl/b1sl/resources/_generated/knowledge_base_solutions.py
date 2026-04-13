from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class KnowledgeBaseSolutionsService(GenericResource["KnowledgeBaseSolution"]):
    """This entity enables you to manipulate 'KnowledgeBaseSolutions'. It represents the knowledge base solutions in the Service module."""
    endpoint = "KnowledgeBaseSolutions"
    
    def __init__(self, adapter):
        from ...models._generated._types import KnowledgeBaseSolution
        self.model = KnowledgeBaseSolution
        super().__init__(adapter)
