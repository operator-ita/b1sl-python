from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class NotaFiscalCFOPService(GenericResource["NotaFiscalCFOP"]):
    """This entity enables you to manipulate 'NotaFiscalCFOP'."""
    endpoint = "NotaFiscalCFOP"
    
    def __init__(self, adapter):
        from ...models._generated._types import NotaFiscalCFOP
        self.model = NotaFiscalCFOP
        super().__init__(adapter)
