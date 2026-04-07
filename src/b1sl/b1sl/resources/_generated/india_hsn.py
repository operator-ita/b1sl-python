from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class IndiaHsnService(GenericResource["IndiaHsn"]):
    """This entity enables you to manipulate 'IndiaHsn'."""
    endpoint = "IndiaHsn"

    def __init__(self, adapter):
        from ...models._generated._types import IndiaHsn
        self.model = IndiaHsn
        super().__init__(adapter)
