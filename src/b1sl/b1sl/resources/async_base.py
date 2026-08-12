from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncGenerator, Generic, TypeVar

if TYPE_CHECKING:
    from b1sl.b1sl.schemas.udf import UDFSchema

from b1sl.b1sl.exceptions.exceptions import B1NotFoundError
from b1sl.b1sl.models.base import B1Model
from b1sl.b1sl.models.paginated_result import PaginatedResult
from b1sl.b1sl.pagination import build_next_params, prepare_top_probe
from b1sl.b1sl.resources.base import (
    ODataQuery,
    _build_expand,
    format_entity_key,
    merge_update_headers,
)

if TYPE_CHECKING:
    from b1sl.b1sl.async_rest_adapter import AsyncRestAdapter
    from b1sl.b1sl.resources.odata import AsyncQueryBuilder, ODataField

T = TypeVar("T", bound=B1Model)


class AsyncGenericResource(Generic[T]):
    """Async counterpart of GenericResource for use with AsyncRestAdapter."""

    endpoint: str
    model: type[T]

    def __init__(self, adapter: AsyncRestAdapter) -> None:
        self._adapter = adapter

    async def get_udf_schema(self, table_name: str | None = None) -> "UDFSchema":
        """
        Retrieves the User Defined Field (UDF) schema for this entity asynchronously.
        Returns a UDFSchema wrapper for easy introspection and validation.

        Args:
            table_name: Optional override for the underlying SAP B1 table.
                        If not provided, uses the mapping for elite entities.
        """
        from b1sl.b1sl.models._generated.entities.general import UserFieldMD
        from b1sl.b1sl.resources.base import _UDF_TABLE_MAPPING
        from b1sl.b1sl.schemas.udf import UDFSchema

        target_table = table_name or _UDF_TABLE_MAPPING.get(self.endpoint)
        if not target_table:
            raise ValueError(
                f"No default table mapping known for endpoint '{self.endpoint}'. "
                "Please provide the 'table_name' argument manually (e.g., table_name='@MY_UDO')."
            )

        params = {"$filter": f"TableName eq '{target_table}'"}
        result = await self._adapter.get("UserFieldsMD", ep_params=params)
        data = result.data or {}

        raw_list = [UserFieldMD.model_validate(item) for item in data.get("value", [])]
        return UDFSchema(target_table, raw_list)

    # ── fluent query builder ────────────────────────────────────────────────
    
    def with_schema(self, name: str) -> AsyncQueryBuilder[T]:
        from b1sl.b1sl.resources.odata import AsyncQueryBuilder
        return AsyncQueryBuilder(self).with_schema(name)

    def by_id(self, key: Any) -> AsyncQueryBuilder[T]:
        from b1sl.b1sl.resources.odata import AsyncQueryBuilder

        return AsyncQueryBuilder(self).by_id(key)

    def filter(self, expression: str) -> AsyncQueryBuilder[T]:
        from b1sl.b1sl.resources.odata import AsyncQueryBuilder

        return AsyncQueryBuilder(self).filter(expression)

    def select(self, *fields: str) -> AsyncQueryBuilder[T]:
        from b1sl.b1sl.resources.odata import AsyncQueryBuilder

        return AsyncQueryBuilder(self).select(*fields)

    def top(self, value: int) -> AsyncQueryBuilder[T]:
        from b1sl.b1sl.resources.odata import AsyncQueryBuilder

        return AsyncQueryBuilder(self).top(value)

    def skip(self, value: int) -> AsyncQueryBuilder[T]:
        from b1sl.b1sl.resources.odata import AsyncQueryBuilder

        return AsyncQueryBuilder(self).skip(value)

    def page_size(self, value: int) -> AsyncQueryBuilder[T]:
        from b1sl.b1sl.resources.odata import AsyncQueryBuilder

        return AsyncQueryBuilder(self).page_size(value)

    def orderby(
        self, expression: str | ODataField, desc: bool = False
    ) -> AsyncQueryBuilder[T]:
        from b1sl.b1sl.resources.odata import AsyncQueryBuilder

        return AsyncQueryBuilder(self).orderby(expression, desc=desc)

    def expand(self, value: list[str] | dict[str, list[str]]) -> AsyncQueryBuilder[T]:
        from b1sl.b1sl.resources.odata import AsyncQueryBuilder

        return AsyncQueryBuilder(self).expand(value)

    def apply(self, expression: str) -> AsyncQueryBuilder[T]:
        from b1sl.b1sl.resources.odata import AsyncQueryBuilder

        return AsyncQueryBuilder(self).apply(expression)

    async def list(
        self,
        query: ODataQuery | None = None,
        *,
        params: dict[str, Any] | None = None,
        page_size: int | None = None,
    ) -> PaginatedResult[T]:
        """
        Retrieve a single page of results with pagination metadata.

        The returned :class:`PaginatedResult` behaves like a list (iteration,
        ``len()``, indexing) and exposes ``next_params`` for manual paging::

            page = await client.items.list(query)
            while page.next_params:
                page = await client.items.list(params=page.next_params)

        Args:
            query: OData query options for the first page.
            params: Raw query params — pass ``page.next_params`` to fetch the
                following page. Mutually exclusive with ``query``.
            page_size: SAP server-side page size (``B1S-PageSize`` header). Caps
                how many rows SAP returns per request, independent of ``$top``.

        Note: Use .stream() for automatic pagination across multiple pages.
        """
        if query is not None and params is not None:
            raise ValueError("Pass either 'query' or 'params', not both.")
        request_params = params if params is not None else (query.to_params() if query else {})
        probe_params, top, base_skip = prepare_top_probe(request_params)
        headers = {"B1S-PageSize": str(page_size)} if page_size else None
        result = await self._adapter.get(f"{self.endpoint}", ep_params=probe_params, headers=headers)
        data = result.data or {}
        raw = data.get("value", [])
        next_link = result.next_link
        if top is not None and len(raw) > top:
            # Fence-post: SAP returned the probe's extra row, so more pages exist
            # even though it gave us no nextLink. Truncate and synthesise a cursor.
            raw = raw[:top]
            next_params: dict[str, Any] | None = {**request_params, "$skip": str(base_skip + top)}
        else:
            next_params = build_next_params(request_params, next_link) if next_link else None
        items = [self.model.model_validate(item) for item in raw]
        return PaginatedResult(
            items, metadata=result.metadata, next_params=next_params,
            total_count=result.total_count,
        )

    async def _list_capped(
        self, query: ODataQuery, top: int, page_size: int | None
    ) -> PaginatedResult[T]:
        """Eagerly collect up to ``top`` rows, following ``nextLink`` across server
        pages (``$top`` enforced client-side, never sent to SAP — same contract as
        ``stream()``).

        Async counterpart of ``GenericResource._list_capped``. Backs
        ``AsyncQueryBuilder.execute()`` when ``.top(N)`` is set so ``.top()`` means
        a *total cap* everywhere; ``has_more`` / ``next_skip`` are computed at the
        ``N`` boundary via a one-row overflow probe.
        """
        params = query.to_params()
        params.pop("$top", None)
        base_skip = int(params.get("$skip") or 0)
        headers = {"B1S-PageSize": str(page_size)} if page_size else {}

        collected: list[Any] = []
        metadata: str | None = None
        total_count: int | None = None
        overflow = False
        current_params = dict(params)
        while True:
            result = await self._adapter.get(self.endpoint, ep_params=current_params, headers=headers)
            if metadata is None:
                metadata = result.metadata  # preserve the first page's @odata.context
            if total_count is None:
                total_count = result.total_count
            for raw in (result.data or {}).get("value", []):
                collected.append(raw)
                if len(collected) > top:  # one row beyond the cap → more pages exist
                    overflow = True
                    break
            if overflow or not result.next_link:
                break
            current_params = build_next_params(current_params, result.next_link)

        items = [self.model.model_validate(item) for item in collected[:top]]
        next_params: dict[str, Any] | None = None
        if overflow:
            next_params = {**params, "$skip": str(base_skip + top)}
        return PaginatedResult(
            items, metadata=metadata, next_params=next_params, total_count=total_count
        )

    async def _iter_pages(
        self,
        url: str,
        params: dict,
        headers: dict,
        max_pages: int | None = None,
    ) -> AsyncGenerator[dict, None]:
        """Yield raw item dicts from a paginated OData endpoint, following nextLink.

        Async counterpart of ``GenericResource._iter_pages``.  Shared by
        ``stream()`` and ``AsyncSQLQueriesResource.run_stream()``.
        """
        current_params = params
        pages_fetched = 0
        while True:
            result = await self._adapter.get(url, ep_params=current_params, headers=headers)
            data = result.data or {}
            pages_fetched += 1
            for item in data.get("value", []):
                yield item
            next_link = result.next_link
            if not next_link:
                break
            if max_pages is not None and pages_fetched >= max_pages:
                break
            current_params = build_next_params(current_params, next_link)

    async def stream(
        self,
        query: ODataQuery | None = None,
        page_size: int | None = None,
        max_pages: int | None = None
    ) -> AsyncGenerator[T, None]:
        """
        Execute the query asynchronously and yield individual entities,
        automatically fetching next pages until dataset exhausted or limits hit.

        Note:
            ``.top(N)`` here is a **global cap on total rows yielded**, not a page
            size — use ``page_size`` for the per-request batch. ``$top`` is
            enforced client-side and deliberately NOT sent to SAP: forwarding it
            muddles paging (OData re-applies ``$top`` relative to each page's
            ``$skip`` cursor) without changing the row count, so keeping it off
            makes ``.top()`` an unambiguous global cap.
        """
        params = query.to_params() if query else {}
        # $top is enforced client-side only (see Note above).
        params.pop("$top", None)
        global_top = query.top if query else None
        headers = {"B1S-PageSize": str(page_size)} if page_size else {}
        yielded_count = 0

        async for raw_item in self._iter_pages(self.endpoint, params, headers, max_pages):
            yield self.model.model_validate(raw_item)
            yielded_count += 1
            if global_top is not None and yielded_count >= global_top:
                return

    async def count(self) -> int:
        """GET Endpoint/$count"""
        result = await self._adapter.get(f"{self.endpoint}/$count")
        return int(result.data)

    async def get_raw(
        self,
        key: Any,
        select: list[str] | None = None,
        expand: list[str] | dict[str, list[str]] | None = None,
        *,
        headers: dict | None = None,
    ) -> dict[str, Any]:
        """GET a single entity as the raw wire dict — no model validation.

        Async counterpart of :meth:`GenericResource.get_raw`: values arrive
        exactly as SAP sent them (``"tYES"`` strings, legacy ``/Date(ms)/``
        dates, every field SAP returned). Pair with ``update(key, dict)`` for
        byte-exact round-trips. ETag caching still applies (adapter-level).
        """
        params: dict[str, str] = {}
        if select:
            select_fields: list[str] = list(select)
            params["$select"] = ",".join(str(f) for f in select_fields)
        if expand:
            params["$expand"] = _build_expand(expand)

        id_str = format_entity_key(key)
        result = await self._adapter.get(
            f"{self.endpoint}({id_str})", ep_params=params, headers=headers
        )
        return result.data

    async def get(
        self,
        key: Any,
        select: list[str] | None = None,
        expand: list[str] | dict[str, list[str]] | None = None,
        *,
        headers: dict | None = None,
    ) -> T:
        return self.model.model_validate(
            await self.get_raw(key, select, expand, headers=headers)
        )

    async def exists(self, key: Any) -> bool:
        """Check if an entity exists by attempting to fetch it."""
        id_str = format_entity_key(key)
        try:
            await self._adapter.get(f"{self.endpoint}({id_str})")
            return True
        except B1NotFoundError:
            return False

    async def create(self, entity: T, *, headers: dict | None = None) -> T:
        # POST: send all fields that are not None (SAP requires complete payloads on create).
        # to_api_payload() uses exclude_unset, which is wrong for create — use model_dump
        # but still encode booleans by delegating through B1Model serialisation.
        payload = entity.model_dump(exclude_none=True, by_alias=True)
        # Re-encode booleans (model_dump returns Python bools, SAP needs tYES/tNO)
        from b1sl.b1sl.models.base import encode_sap_value
        encoded = {k: encode_sap_value(v) for k, v in payload.items()}
        result = await self._adapter.post(
            f"{self.endpoint}", data=encoded, headers=headers
        )
        return self.model.model_validate(result.data)

    async def update(
        self,
        key: Any,
        entity: T | dict[str, Any],
        *,
        headers: dict | None = None,
        replace_collections: bool = False,
    ) -> None:
        # PATCH: a model (T) is a surgical delta — to_api_payload()
        # (exclude_unset) sends only the fields explicitly set, with SAP
        # value encoding. A dict is a verbatim passthrough — sent exactly as
        # given (SAP aliases + SAP-encoded values are the caller's job).
        #
        # replace_collections=True sends B1S-ReplaceCollectionsOnPatch so SAP
        # replaces child collections wholesale instead of merging them.
        #
        # After a successful PATCH, the server-side ETag changes but SAP SL
        # returns 204 No Content without a new ETag header. The adapter
        # proactively invalidates the stale cache entry on every successful
        # write, so the next PATCH or DELETE does not hit a predictable 412.
        id_str = format_entity_key(key)
        payload = entity if isinstance(entity, dict) else entity.to_api_payload()
        await self._adapter.patch(
            f"{self.endpoint}({id_str})",
            data=payload,
            headers=merge_update_headers(headers, replace_collections),
        )

    async def delete(self, key: Any, *, headers: dict | None = None) -> None:
        id_str = format_entity_key(key)
        await self._adapter.delete(f"{self.endpoint}({id_str})", headers=headers)

    # ── Actions / Functions ───────────────────────────────────────────────────

    async def action(
        self,
        key: Any,
        name: str,
        payload: dict | None = None,
        *,
        params: dict | None = None,
        headers: dict | None = None,
        method: str = "POST",
    ) -> Any:
        """Invoke a bound action or function on a keyed entity.

        Covers two SAP OData patterns:
        - POST Endpoint('key')/ActionName  (default, side-effecting actions)
        - GET  Endpoint('key')/FunctionName (read-only bounded functions, e.g. /List)

        The full response ``data`` dict is returned — callers needing
        ``@odata.nextLink`` should inspect it directly.

        Example::

            invoices = b1.get_resource(en.Document, "Invoices")
            await invoices.action(123, "Cancel")
        """
        id_str = format_entity_key(key)
        url = f"{self.endpoint}({id_str})/{name}"
        if method == "GET":
            result = await self._adapter.get(url, ep_params=params, headers=headers)
        else:
            result = await self._adapter.post(
                url, ep_params=params, data=payload or {}, headers=headers
            )
        return result.data if result else None

    async def function(self, name: str, params: dict | None = None) -> Any:
        """GET Endpoint/FunctionName(params) — unkeyed, read-only function."""
        result = await self._adapter.get(f"{self.endpoint}/{name}", ep_params=params or {})
        return result.data if result else None

    # Backwards-compatible aliases (pre-public-API names).
    _action = action
    _function = function
