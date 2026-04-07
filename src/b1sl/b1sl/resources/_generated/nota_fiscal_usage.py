from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class NotaFiscalUsageService(GenericResource["NotaFiscalUsage"]):
    """This entity enables you to manipulate 'NotaFiscalUsage'."""
    endpoint = "NotaFiscalUsage"

    def __init__(self, adapter):
        from ...models._generated._types import NotaFiscalUsage
        self.model = NotaFiscalUsage
        super().__init__(adapter)
