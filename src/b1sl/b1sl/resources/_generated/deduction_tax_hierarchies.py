from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class DeductionTaxHierarchiesService(GenericResource["DeductionTaxHierarchy"]):
    """This entity enables you to manipulate 'DeductionTaxHierarchies'. It defines taxation levels to withhold from payments to vendors."""
    endpoint = "DeductionTaxHierarchies"

    def __init__(self, adapter):
        from ...models._generated._types import DeductionTaxHierarchy
        self.model = DeductionTaxHierarchy
        super().__init__(adapter)
