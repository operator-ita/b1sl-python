from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class QueryService(GenericResource[Any]):
    endpoint = "QueryService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def post_query(self, payload: dict | None = None) -> Any:
        """POST QueryService_PostQuery
        Invoke the method 'PostQuery' on this service. To fully comply with OData, Service Layer exposes a new query service for the row level filter, which is implemented based on the $crossjoin capabilities by separating the QueryPath and QueryOption in the query URL.

        Example:
        ```json
        {
            "QueryOption": "$expand=Orders($select=DocEntry, DocNum),Orders/DocumentLines($select=ItemCode,LineNum)&$filter=Orders/DocEntry eq Orders/DocumentLines/DocEntry and Orders/DocEntry ge 3 and Orders/DocumentLines/LineNum eq 0",
            "QueryPath": "$crossjoin(Orders,Orders/DocumentLines)"
        }
        ```
        """
        return self._adapter.post("QueryService_PostQuery", data=payload)
