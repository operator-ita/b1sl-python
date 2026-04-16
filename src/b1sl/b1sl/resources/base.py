"""
b1sl.b1sl.resources.base
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unified base classes for SAP B1 resources.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Generic, TypeVar

if TYPE_CHECKING:
    from b1sl.b1sl.resources.odata import QueryBuilder

from b1sl.b1sl.adapter_protocol import RestAdapterProtocol
from b1sl.b1sl.exceptions.exceptions import B1NotFoundError
from b1sl.b1sl.models.base import B1Model

T = TypeVar("T", bound=B1Model)


def _build_expand(expand: list[str] | dict[str, list[str]] | None) -> str | None:
    """
    Normalise $expand parameter to OData string syntax.
    Supports:
    - list: ["A", "B"] -> "A,B"
    - dict: {"Nav": ["F1", "F2"]} -> "Nav($select=F1,F2)"
    - str: "Activities" -> "Activities" (if passed manually)
    """
    if not expand:
        return None
    if isinstance(expand, str):
        return expand
    if isinstance(expand, list):
        return ",".join(str(f) for f in expand)

    # dict: {"BusinessPartner": ["CardCode"]} -> "BusinessPartner($select=CardCode)"
    parts = []
    for nav, fields in expand.items():
        nav_str = str(nav)  # StrEnum -> "BusinessPartner"
        if fields:
            sel = ",".join(str(f) for f in fields)
            parts.append(f"{nav_str}($select={sel})")
        else:
            parts.append(nav_str)
    return ",".join(parts)


@dataclass
class ODataQuery:
    """Typed container for all SAP SL query options."""

    filter: str | None = None
    orderby: str | None = None
    select: list[str] | None = None
    skip: int | None = None
    top: int | None = None
    expand: list[str] | dict[str, list[str]] | None = None
    count: bool = False  # $count=true inline

    def to_params(self) -> dict[str, str]:
        p: dict[str, str] = {}
        if self.filter:
            p["$filter"] = self.filter
        if self.orderby:
            p["$orderby"] = self.orderby
        if self.select:
            p["$select"] = ",".join(str(f) for f in self.select)
        if self.skip is not None:
            p["$skip"] = str(self.skip)
        if self.top is not None:
            p["$top"] = str(self.top)
        if self.expand:
            p["$expand"] = _build_expand(self.expand)
        if self.count:
            p["$count"] = "true"
        return p


class GenericResource(Generic[T]):
    endpoint: str  # e.g. "BusinessPartners"
    model: type[T]

    def __init__(self, adapter: RestAdapterProtocol) -> None:
        self._adapter = adapter

    # ── fluent query builder ────────────────────────────────────────────────
    
    def by_id(self, key: Any) -> QueryBuilder[T]:
        from b1sl.b1sl.resources.odata import QueryBuilder
        return QueryBuilder(self).by_id(key)

    def filter(self, expression: str) -> QueryBuilder[T]:
        from b1sl.b1sl.resources.odata import QueryBuilder
        return QueryBuilder(self).filter(expression)

    def select(self, *fields: str) -> QueryBuilder[T]:
        from b1sl.b1sl.resources.odata import QueryBuilder
        return QueryBuilder(self).select(*fields)

    def top(self, value: int) -> QueryBuilder[T]:
        from b1sl.b1sl.resources.odata import QueryBuilder
        return QueryBuilder(self).top(value)

    def skip(self, value: int) -> QueryBuilder[T]:
        from b1sl.b1sl.resources.odata import QueryBuilder
        return QueryBuilder(self).skip(value)

    def orderby(self, expression: str) -> QueryBuilder[T]:
        from b1sl.b1sl.resources.odata import QueryBuilder
        return QueryBuilder(self).orderby(expression)

    def expand(self, value: list[str] | dict[str, list[str]]) -> QueryBuilder[T]:
        from b1sl.b1sl.resources.odata import QueryBuilder
        return QueryBuilder(self).expand(value)

    # ── Collection ───────────────────────────────────────────────────────────

    def list(self, query: ODataQuery | None = None) -> list[T]:
        params = query.to_params() if query else {}
        # We assume the adapter returns a RestResponse with a .data dict
        result = self._adapter.get(f"{self.endpoint}", ep_params=params)
        data = result.data or {}
        return [self.model.model_validate(item) for item in data.get("value", [])]

    def count(self) -> int:
        """GET Endpoint/$count"""
        result = self._adapter.get(f"{self.endpoint}/$count")
        return int(result.data)

    # ── Single entity ─────────────────────────────────────────────────────────

    def get(
        self,
        key: Any,
        select: list[str] | None = None,
        expand: list[str] | dict[str, list[str]] | None = None,
    ) -> T:
        params: dict[str, str] = {}
        if select:
            params["$select"] = ",".join(str(f) for f in select)
        if expand:
            params["$expand"] = _build_expand(expand)

        id_str = f"'{key}'" if isinstance(key, str) else str(key)
        result = self._adapter.get(f"{self.endpoint}({id_str})", ep_params=params)
        return self.model.model_validate(result.data)

    def exists(self, key: Any) -> bool:
        """Check if an entity exists by attempting to fetch it.
        
        Note: We avoid $select=1 as it's not supported by all SAP SL versions/entities
        and results in 'SAP Error 201: Not supported query string'.
        """
        id_str = f"'{key}'" if isinstance(key, str) else str(key)
        try:
            self._adapter.get(f"{self.endpoint}({id_str})")
            return True
        except B1NotFoundError:
            return False

    # ── Mutations ─────────────────────────────────────────────────────────────

    def create(self, entity: T) -> T:
        # POST: send all non-None fields. SAP requires a complete payload on creation.
        # model_dump returns native Python bools; re-encode them to tYES/tNO.
        from b1sl.b1sl.models.base import _SAP_NO, _SAP_YES

        payload = entity.model_dump(exclude_none=True, by_alias=True)
        encoded = {
            k: (_SAP_YES if v is True else _SAP_NO if v is False else v)
            for k, v in payload.items()
        }
        result = self._adapter.post(f"{self.endpoint}", data=encoded)
        return self.model.model_validate(result.data)

    def update(self, key: Any, entity: T) -> None:
        """PATCH — partial update, SAP SL returns 204 No Content.

        Uses to_api_payload() (exclude_unset) so only fields explicitly set
        by the developer are sent — the correct delta semantics for PATCH.
        Booleans are automatically encoded to tYES/tNO.

        After a successful PATCH, the server-side ETag is guaranteed to have
        changed (a new version was created), but SAP SL returns 204 No Content
        without a new ETag header. Keeping the old (now stale) ETag in cache
        would cause a predictable 412 conflict on the next PATCH or DELETE.
        We proactively invalidate it so the next mutating call either sends no
        ETag (blind write) or forces a fresh GET first.
        """
        id_str = f"'{key}'" if isinstance(key, str) else str(key)
        endpoint_path = f"/{self.endpoint}({id_str})"
        self._adapter.patch(
            f"{self.endpoint}({id_str})",
            data=entity.to_api_payload(),
        )
        # Proactively invalidate the stale ETag: SAP issued a 204 with no
        # new ETag header, so anything in cache is now a lie.
        self._adapter._clear_etag(endpoint_path)

    def delete(self, key: Any) -> None:
        id_str = f"'{key}'" if isinstance(key, str) else str(key)
        self._adapter.delete(f"{self.endpoint}({id_str})")

    # ── Actions / Functions ───────────────────────────────────────────────────

    def _action(self, key: Any, name: str, payload: dict | None = None) -> Any:
        """POST Endpoint(key)/ActionName"""
        id_str = f"'{key}'" if isinstance(key, str) else str(key)
        result = self._adapter.post(
            f"{self.endpoint}({id_str})/{name}", data=payload or {}
        )
        return result.data if result else None

    def _function(self, name: str, params: dict | None = None) -> Any:
        """GET Endpoint/FunctionName(params)"""
        result = self._adapter.get(f"{self.endpoint}/{name}", ep_params=params or {})
        return result.data if result else None
