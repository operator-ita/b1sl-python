"""
b1sl.b1sl.resources.crossjoin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``$crossjoin`` builder for SAP Service Layer (B1 9.2 patch 07+, SAP HANA only).

Cross-joins query across entity sets with no predefined navigation properties.
The URL path is the resource identifier: ``/b1s/v1/$crossjoin(Entity1,Entity2,...)``.

Usage (sync)::

    rows = (
        client.crossjoin("Orders", "BusinessPartners")
        .expand({"Orders": ["DocEntry", "DocNum"], "BusinessPartners": ["CardCode"]})
        .filter("Orders/CardCode eq BusinessPartners/CardCode and Orders/DocNum le 3")
        .execute()
    )

Usage (async)::

    rows = await (
        client.crossjoin("Orders", "BusinessPartners")
        .expand({"Orders": ["DocEntry", "DocNum"], "BusinessPartners": ["CardCode"]})
        .filter("Orders/CardCode eq BusinessPartners/CardCode")
        .execute()
    )

Aggregation variant::

    rows = (
        client.crossjoin("Orders", "BusinessPartners")
        .apply(
            "filter(Orders/CardCode eq BusinessPartners/CardCode)"
            "/groupby((BusinessPartners/CardCode),"
            "aggregate(Orders(DocNum with max as MaxDocNum)))"
        )
        .execute()
    )

Rules:
- At least 2 entity names are required.
- A bare crossjoin without ``$expand`` or ``$apply`` will return 400 from SAP.
  This builder validates proactively and raises ``ValueError`` before the request.
- Navigation paths use ``EntityName/FieldName`` syntax throughout.
- Arithmetic in ``$expand`` select (``add``, ``sub``, ``mul``, ``div``) is passed
  verbatim in the select string: ``"DocEntry mul (DocNum sub 1) as DocSeq"``.
- Results are ``list[dict]`` (raw SAP ComplexType) — no entity model applies.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncGenerator, Generator

from b1sl.b1sl.pagination import build_next_params
from b1sl.b1sl.resources.base import _build_expand

if TYPE_CHECKING:
    from b1sl.b1sl.adapter_protocol import RestAdapterProtocol
    from b1sl.b1sl.async_rest_adapter import AsyncRestAdapter


class CrossJoinQueryBuilder:
    """Sync fluent builder for ``$crossjoin`` queries."""

    def __init__(self, adapter: RestAdapterProtocol, *entities: str) -> None:
        if len(entities) < 2:
            raise ValueError(
                f"$crossjoin requires at least 2 entity names, got {len(entities)}. "
                "Example: client.crossjoin('Orders', 'BusinessPartners')"
            )
        self._adapter = adapter
        self._entities = entities
        self._expand: dict[str, list[str]] | None = None
        self._filter: str | None = None
        self._apply: str | None = None
        self._orderby: str | None = None
        self._top: int | None = None
        self._skip: int | None = None

    # ── path ──────────────────────────────────────────────────────────────────

    @property
    def _path(self) -> str:
        return "$crossjoin(" + ",".join(self._entities) + ")"

    # ── fluent methods ────────────────────────────────────────────────────────

    def expand(self, fields: dict[str, list[str]]) -> CrossJoinQueryBuilder:
        """Project fields per entity.

        Keys are entity names; values are field lists.  Arithmetic expressions
        are passed verbatim in the list:
        ``{"Orders": ["DocEntry mul (DocNum sub 1) as DocSeq"]}``
        """
        self._expand = fields
        return self

    def filter(self, expression: str) -> CrossJoinQueryBuilder:
        """Set ``$filter``.  Navigation paths use ``EntityName/FieldName`` syntax."""
        self._filter = expression
        return self

    def apply(self, expression: str) -> CrossJoinQueryBuilder:
        """Set ``$apply`` for aggregation/groupby.

        Example::

            .apply(
                "filter(Orders/CardCode eq BusinessPartners/CardCode)"
                "/groupby((BusinessPartners/CardCode),"
                "aggregate(Orders(DocNum with max as MaxDocNum)))"
            )
        """
        self._apply = expression
        return self

    def orderby(self, expression: str, desc: bool = False) -> CrossJoinQueryBuilder:
        expr = expression if not desc else f"{expression} desc"
        self._orderby = expr
        return self

    def top(self, value: int) -> CrossJoinQueryBuilder:
        self._top = value
        return self

    def skip(self, value: int) -> CrossJoinQueryBuilder:
        self._skip = value
        return self

    # ── params ────────────────────────────────────────────────────────────────

    def _build_params(self) -> dict[str, str]:
        p: dict[str, str] = {}
        if self._expand:
            expanded = _build_expand(self._expand)
            if expanded:
                p["$expand"] = expanded
        if self._filter:
            p["$filter"] = self._filter
        if self._apply:
            p["$apply"] = self._apply
        if self._orderby:
            p["$orderby"] = self._orderby
        if self._top is not None:
            p["$top"] = str(self._top)
        if self._skip is not None:
            p["$skip"] = str(self._skip)
        return p

    def _validate(self) -> None:
        if not self._expand and not self._apply:
            entities = ", ".join(f"'{e}'" for e in self._entities)
            raise ValueError(
                f"$crossjoin({', '.join(self._entities)}) has no $expand or $apply. "
                "SAP SL returns 400 for a bare crossjoin. "
                "Add .expand({...}) to project fields or .apply(...) for aggregation. "
                f"Entities given: {entities}."
            )

    # ── execution ─────────────────────────────────────────────────────────────

    def execute(self) -> list[dict[str, Any]]:
        """Execute the crossjoin query and return all rows from the first page."""
        self._validate()
        result = self._adapter.get(self._path, ep_params=self._build_params())
        data = result.data or {}
        return list(data.get("value", []))

    def stream(
        self,
        page_size: int | None = None,
        max_pages: int | None = None,
    ) -> Generator[dict[str, Any], None, None]:
        """Execute and stream all rows, following ``odata.nextLink`` across pages."""
        self._validate()
        params = self._build_params()
        headers = {"B1-PageSize": str(page_size)} if page_size else {}
        global_top = self._top
        yielded = 0

        current_params = params
        pages_fetched = 0
        while True:
            result = self._adapter.get(self._path, ep_params=current_params, headers=headers)
            data = result.data or {}
            pages_fetched += 1
            for item in data.get("value", []):
                yield item
                yielded += 1
                if global_top is not None and yielded >= global_top:
                    return
            next_link = result.next_link
            if not next_link:
                break
            if max_pages is not None and pages_fetched >= max_pages:
                break
            current_params = build_next_params(current_params, next_link)

    def first(self) -> dict[str, Any] | None:
        """Return the first row or ``None``."""
        rows = self.top(1).execute()
        return rows[0] if rows else None


class AsyncCrossJoinQueryBuilder:
    """Async fluent builder for ``$crossjoin`` queries."""

    def __init__(self, adapter: AsyncRestAdapter, *entities: str) -> None:
        if len(entities) < 2:
            raise ValueError(
                f"$crossjoin requires at least 2 entity names, got {len(entities)}. "
                "Example: client.crossjoin('Orders', 'BusinessPartners')"
            )
        self._adapter = adapter
        self._entities = entities
        self._expand: dict[str, list[str]] | None = None
        self._filter: str | None = None
        self._apply: str | None = None
        self._orderby: str | None = None
        self._top: int | None = None
        self._skip: int | None = None

    @property
    def _path(self) -> str:
        return "$crossjoin(" + ",".join(self._entities) + ")"

    def expand(self, fields: dict[str, list[str]]) -> AsyncCrossJoinQueryBuilder:
        self._expand = fields
        return self

    def filter(self, expression: str) -> AsyncCrossJoinQueryBuilder:
        self._filter = expression
        return self

    def apply(self, expression: str) -> AsyncCrossJoinQueryBuilder:
        self._apply = expression
        return self

    def orderby(self, expression: str, desc: bool = False) -> AsyncCrossJoinQueryBuilder:
        expr = expression if not desc else f"{expression} desc"
        self._orderby = expr
        return self

    def top(self, value: int) -> AsyncCrossJoinQueryBuilder:
        self._top = value
        return self

    def skip(self, value: int) -> AsyncCrossJoinQueryBuilder:
        self._skip = value
        return self

    def _build_params(self) -> dict[str, str]:
        p: dict[str, str] = {}
        if self._expand:
            expanded = _build_expand(self._expand)
            if expanded:
                p["$expand"] = expanded
        if self._filter:
            p["$filter"] = self._filter
        if self._apply:
            p["$apply"] = self._apply
        if self._orderby:
            p["$orderby"] = self._orderby
        if self._top is not None:
            p["$top"] = str(self._top)
        if self._skip is not None:
            p["$skip"] = str(self._skip)
        return p

    def _validate(self) -> None:
        if not self._expand and not self._apply:
            raise ValueError(
                f"$crossjoin({', '.join(self._entities)}) has no $expand or $apply. "
                "SAP SL returns 400 for a bare crossjoin. "
                "Add .expand({...}) to project fields or .apply(...) for aggregation."
            )

    async def execute(self) -> list[dict[str, Any]]:
        """Execute the crossjoin query and return all rows from the first page."""
        self._validate()
        result = await self._adapter.get(self._path, ep_params=self._build_params())
        data = result.data or {}
        return list(data.get("value", []))

    async def stream(
        self,
        page_size: int | None = None,
        max_pages: int | None = None,
    ) -> AsyncGenerator[dict[str, Any], None]:
        """Stream all rows asynchronously, following ``odata.nextLink``."""
        self._validate()
        params = self._build_params()
        headers = {"B1-PageSize": str(page_size)} if page_size else {}
        global_top = self._top
        yielded = 0

        current_params = params
        pages_fetched = 0
        while True:
            result = await self._adapter.get(self._path, ep_params=current_params, headers=headers)
            data = result.data or {}
            pages_fetched += 1
            for item in data.get("value", []):
                yield item
                yielded += 1
                if global_top is not None and yielded >= global_top:
                    return
            next_link = result.next_link
            if not next_link:
                break
            if max_pages is not None and pages_fetched >= max_pages:
                break
            current_params = build_next_params(current_params, next_link)

    async def first(self) -> dict[str, Any] | None:
        """Return the first row or ``None``."""
        rows = await self.top(1).execute()
        return rows[0] if rows else None


# ── QueryService (POST-based row-level filter) ────────────────────────────────


class QueryServiceBuilder:
    """Sync builder for ``QueryService_PostQuery`` (SAP HANA only, B1 9.2 PL11+).

    Joins a document header with its navigation lines for row-level filtering.
    Unlike ``CrossJoinQueryBuilder`` (GET), this sends a POST request so the
    ``QueryPath`` and ``QueryOption`` stay in the body instead of the URL.

    Usage::

        rows = (
            client.query_service("$crossjoin(Orders,Orders/DocumentLines)")
            .expand({
                "Orders": ["DocEntry", "DocNum"],
                "Orders/DocumentLines": ["ItemCode", "LineNum"],
            })
            .filter(
                "Orders/DocEntry eq Orders/DocumentLines/DocEntry"
                " and Orders/DocumentLines/ItemCode eq 'WIDGET'"
            )
            .execute()
        )

    Rules:
    - At least ``expand`` or ``apply`` must be provided — SAP returns 400 otherwise.
    - Navigation paths in ``QueryPath`` use ``Entity/NavProperty`` syntax.
    - Pagination (``odata.nextLink``) is not supported for POST — use ``top``/``skip``
      for manual paging if needed.
    - Response content-type is ``text/plain`` but contains valid JSON.
    """

    def __init__(self, adapter: RestAdapterProtocol, query_path: str) -> None:
        if not query_path:
            raise ValueError("query_path must be a non-empty string.")
        self._adapter = adapter
        self._query_path = query_path
        self._expand: dict[str, list[str]] | None = None
        self._filter: str | None = None
        self._apply: str | None = None
        self._orderby: str | None = None
        self._top: int | None = None
        self._skip: int | None = None

    # ── fluent methods ────────────────────────────────────────────────────────

    def expand(self, fields: dict[str, list[str]]) -> QueryServiceBuilder:
        """Project fields per entity/navigation key.

        Keys can be entity names or navigation paths::

            .expand({
                "Orders": ["DocEntry", "DocNum"],
                "Orders/DocumentLines": ["ItemCode", "LineNum"],
            })
        """
        self._expand = fields
        return self

    def filter(self, expression: str) -> QueryServiceBuilder:
        """Set ``$filter``.  Use navigation paths: ``Entity/Field``."""
        self._filter = expression
        return self

    def apply(self, expression: str) -> QueryServiceBuilder:
        """Set ``$apply`` for server-side aggregation/groupby."""
        self._apply = expression
        return self

    def orderby(self, expression: str, desc: bool = False) -> QueryServiceBuilder:
        self._orderby = expression if not desc else f"{expression} desc"
        return self

    def top(self, value: int) -> QueryServiceBuilder:
        self._top = value
        return self

    def skip(self, value: int) -> QueryServiceBuilder:
        self._skip = value
        return self

    # ── internal ──────────────────────────────────────────────────────────────

    def _build_params(self) -> dict[str, str]:
        p: dict[str, str] = {}
        if self._expand:
            expanded = _build_expand(self._expand)
            if expanded:
                p["$expand"] = expanded
        if self._filter:
            p["$filter"] = self._filter
        if self._apply:
            p["$apply"] = self._apply
        if self._orderby:
            p["$orderby"] = self._orderby
        if self._top is not None:
            p["$top"] = str(self._top)
        if self._skip is not None:
            p["$skip"] = str(self._skip)
        return p

    def _build_query_option(self) -> str:
        """Serialize params as an unencoded query string for the POST body."""
        return "&".join(f"{k}={v}" for k, v in self._build_params().items())

    def _validate(self) -> None:
        if not self._expand and not self._apply:
            raise ValueError(
                f"QueryService query_path={self._query_path!r} has no $expand or $apply. "
                "SAP SL returns 400 without field projection. "
                "Add .expand({...}) or .apply(...)."
            )

    # ── execution ─────────────────────────────────────────────────────────────

    def execute(self) -> list[dict[str, Any]]:
        """POST to ``QueryService_PostQuery`` and return all rows."""
        self._validate()
        payload = {
            "QueryPath": self._query_path,
            "QueryOption": self._build_query_option(),
        }
        result = self._adapter.post("QueryService_PostQuery", data=payload)
        data = result.data or {}
        # SAP returns text/plain; httpx.json() parses it, but guard for a
        # double-encoded string response just in case.
        if isinstance(data, str):
            import json as _json
            data = _json.loads(data)
        return list(data.get("value", []))

    def first(self) -> dict[str, Any] | None:
        """Return the first row or ``None``."""
        rows = self.top(1).execute()
        return rows[0] if rows else None


class AsyncQueryServiceBuilder:
    """Async counterpart of :class:`QueryServiceBuilder`."""

    def __init__(self, adapter: AsyncRestAdapter, query_path: str) -> None:
        if not query_path:
            raise ValueError("query_path must be a non-empty string.")
        self._adapter = adapter
        self._query_path = query_path
        self._expand: dict[str, list[str]] | None = None
        self._filter: str | None = None
        self._apply: str | None = None
        self._orderby: str | None = None
        self._top: int | None = None
        self._skip: int | None = None

    def expand(self, fields: dict[str, list[str]]) -> AsyncQueryServiceBuilder:
        self._expand = fields
        return self

    def filter(self, expression: str) -> AsyncQueryServiceBuilder:
        self._filter = expression
        return self

    def apply(self, expression: str) -> AsyncQueryServiceBuilder:
        self._apply = expression
        return self

    def orderby(self, expression: str, desc: bool = False) -> AsyncQueryServiceBuilder:
        self._orderby = expression if not desc else f"{expression} desc"
        return self

    def top(self, value: int) -> AsyncQueryServiceBuilder:
        self._top = value
        return self

    def skip(self, value: int) -> AsyncQueryServiceBuilder:
        self._skip = value
        return self

    def _build_params(self) -> dict[str, str]:
        p: dict[str, str] = {}
        if self._expand:
            expanded = _build_expand(self._expand)
            if expanded:
                p["$expand"] = expanded
        if self._filter:
            p["$filter"] = self._filter
        if self._apply:
            p["$apply"] = self._apply
        if self._orderby:
            p["$orderby"] = self._orderby
        if self._top is not None:
            p["$top"] = str(self._top)
        if self._skip is not None:
            p["$skip"] = str(self._skip)
        return p

    def _build_query_option(self) -> str:
        return "&".join(f"{k}={v}" for k, v in self._build_params().items())

    def _validate(self) -> None:
        if not self._expand and not self._apply:
            raise ValueError(
                f"QueryService query_path={self._query_path!r} has no $expand or $apply. "
                "SAP SL returns 400 without field projection. "
                "Add .expand({...}) or .apply(...)."
            )

    async def execute(self) -> list[dict[str, Any]]:
        """POST to ``QueryService_PostQuery`` and return all rows."""
        self._validate()
        payload = {
            "QueryPath": self._query_path,
            "QueryOption": self._build_query_option(),
        }
        result = await self._adapter.post("QueryService_PostQuery", data=payload)
        data = result.data or {}
        if isinstance(data, str):
            import json as _json
            data = _json.loads(data)
        return list(data.get("value", []))

    async def first(self) -> dict[str, Any] | None:
        """Return the first row or ``None``."""
        rows = await self.top(1).execute()
        return rows[0] if rows else None
