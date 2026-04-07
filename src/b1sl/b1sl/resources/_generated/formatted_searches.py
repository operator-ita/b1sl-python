from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class FormattedSearchesService(GenericResource["FormattedSearch"]):
    """This entity enables you to manipulate 'FormattedSearches'. It allows to assign a formatted search function to a specified field, so that SAP Business One users can enter values, originated by a pre-defined search process, to the field."""
    endpoint = "FormattedSearches"

    def __init__(self, adapter):
        from ...models._generated._types import FormattedSearch
        self.model = FormattedSearch
        super().__init__(adapter)
