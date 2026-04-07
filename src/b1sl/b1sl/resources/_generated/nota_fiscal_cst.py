from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class NotaFiscalCSTService(GenericResource["NotaFiscalCST"]):
    """This entity enables you to manipulate 'NotaFiscalCST'."""
    endpoint = "NotaFiscalCST"
    
    def __init__(self, adapter):
        from ...models._generated._types import NotaFiscalCST
        self.model = NotaFiscalCST
        super().__init__(adapter)
