"""
b1sl.b1sl.resources.base
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unified base classes for SAP B1 resources.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, TypeVar

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
        """Check if an entity exists by attempting to fetch its minimal representation."""
        id_str = f"'{key}'" if isinstance(key, str) else str(key)
        try:
            # We use a minimal $select to avoid fetching massive payloads
            self._adapter.get(f"{self.endpoint}({id_str})", ep_params={"$select": "1"})
            return True
        except B1NotFoundError:
            return False

    # ── Mutations ─────────────────────────────────────────────────────────────

    def create(self, entity: T) -> T:
        result = self._adapter.post(
            f"{self.endpoint}", data=entity.model_dump(exclude_none=True, by_alias=True)
        )
        return self.model.model_validate(result.data)

    def update(self, key: Any, entity: T) -> None:
        """PATCH — partial update, SAP SL returns 204 No Content."""
        id_str = f"'{key}'" if isinstance(key, str) else str(key)
        self._adapter.patch(
            f"{self.endpoint}({id_str})",
            data=entity.model_dump(exclude_none=True, by_alias=True),
        )

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
