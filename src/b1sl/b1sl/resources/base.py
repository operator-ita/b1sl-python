"""
b1sl.b1sl.resources.base
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unified base classes for SAP B1 resources.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Generator, Generic, TypeVar

if TYPE_CHECKING:
    from b1sl.b1sl.resources.odata import ODataField, QueryBuilder
    from b1sl.b1sl.schemas.udf import UDFSchema

from b1sl.b1sl.adapter_protocol import RestAdapterProtocol
from b1sl.b1sl.exceptions.exceptions import B1NotFoundError
from b1sl.b1sl.models.base import B1Model
from b1sl.b1sl.models.paginated_result import PaginatedResult
from b1sl.b1sl.pagination import build_next_params, prepare_top_probe

T = TypeVar("T", bound=B1Model)


def format_entity_key(key) -> str:
    """Format an entity key for interpolation into an OData resource path.

    String keys are single-quoted with OData escaping (' -> ''), so a key
    containing quotes cannot break out of the path literal (defense in depth —
    SAP rejects malformed paths anyway, but keys can flow from user input).
    """
    if isinstance(key, str):
        escaped = key.replace("'", "''")
        return f"'{escaped}'"
    return str(key)


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
    apply: str | None = None  # $apply for aggregation/groupby (SAP HANA only)

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
        if self.apply:
            p["$apply"] = self.apply
        return p


# Mapping of Elite endpoints to their primary SAP B1 database tables for UDF lookups
_UDF_TABLE_MAPPING = {
    "BusinessPartners": "OCRD",
    "Items": "OITM",
    "Activities": "OCLG",
    "Quotations": "OQUT",
    "Orders": "ORDR",
    "DeliveryNotes": "ODLN",
    "Invoices": "OINV",
    "Returns": "ORDN",
    "ReturnRequest": "ORRR",
    "CreditNotes": "ORIN",
    "DownPayments": "ODPI",
    "GoodsReturnRequest": "OPRR",
    "PurchaseRequests": "OPRQ",
    "PurchaseQuotations": "OPQT",
    "PurchaseOrders": "OPOR",
    "PurchaseDeliveryNotes": "OPDN",
    "PurchaseInvoices": "OPCH",
    "PurchaseReturns": "ORPD",
    "PurchaseCreditNotes": "ORPC",
    "InventoryGenEntries": "OIGN",
    "InventoryGenExits": "OIGE",
    "Drafts": "ODRF",
}


class GenericResource(Generic[T]):
    endpoint: str  # e.g. "BusinessPartners"
    model: type[T]

    def __init__(self, adapter: RestAdapterProtocol) -> None:
        self._adapter = adapter

    def get_udf_schema(self, table_name: str | None = None) -> "UDFSchema":
        """
        Retrieves the User Defined Field (UDF) schema for this entity.
        Returns a UDFSchema wrapper for easy introspection and validation.

        Args:
            table_name: Optional override for the underlying SAP B1 table.
                        If not provided, uses the mapping for elite entities.
        """
        from b1sl.b1sl.models._generated.entities.general import UserFieldMD
        from b1sl.b1sl.schemas.udf import UDFSchema

        target_table = table_name or _UDF_TABLE_MAPPING.get(self.endpoint)
        if not target_table:
            raise ValueError(
                f"No default table mapping known for endpoint '{self.endpoint}'. "
                "Please provide the 'table_name' argument manually (e.g., table_name='@MY_UDO')."
            )

        params = {"$filter": f"TableName eq '{target_table}'"}
        result = self._adapter.get("UserFieldsMD", ep_params=params)
        data = result.data or {}

        raw_list = [UserFieldMD.model_validate(item) for item in data.get("value", [])]
        return UDFSchema(target_table, raw_list)

    # ── fluent query builder ────────────────────────────────────────────────
    
    def with_schema(self, name: str) -> QueryBuilder[T]:
        from b1sl.b1sl.resources.odata import QueryBuilder
        return QueryBuilder(self).with_schema(name)

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

    def page_size(self, value: int) -> QueryBuilder[T]:
        from b1sl.b1sl.resources.odata import QueryBuilder
        return QueryBuilder(self).page_size(value)

    def orderby(
        self, expression: str | ODataField, desc: bool = False
    ) -> QueryBuilder[T]:
        from b1sl.b1sl.resources.odata import QueryBuilder
        return QueryBuilder(self).orderby(expression, desc=desc)

    def expand(self, value: list[str] | dict[str, list[str]]) -> QueryBuilder[T]:
        from b1sl.b1sl.resources.odata import QueryBuilder
        return QueryBuilder(self).expand(value)

    def apply(self, expression: str) -> QueryBuilder[T]:
        from b1sl.b1sl.resources.odata import QueryBuilder
        return QueryBuilder(self).apply(expression)

    # ── Collection ───────────────────────────────────────────────────────────

    def list(
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

            page = client.items.list(query)
            while page.next_params:
                page = client.items.list(params=page.next_params)

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
        result = self._adapter.get(f"{self.endpoint}", ep_params=probe_params, headers=headers)
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
        return PaginatedResult(items, metadata=result.metadata, next_params=next_params)

    def _iter_pages(
        self,
        url: str,
        params: dict,
        headers: dict,
        max_pages: int | None = None,
    ) -> Generator[dict, None, None]:
        """Yield raw item dicts from a paginated OData endpoint, following nextLink.

        Shared pagination primitive used by both ``stream()`` (typed entity iteration)
        and ``SQLQueriesResource.run_stream()`` (raw dict iteration).  Stops when SAP
        returns no ``@odata.nextLink`` / ``odata.nextLink``, or when ``max_pages`` is hit.
        """
        current_params = params
        pages_fetched = 0
        while True:
            result = self._adapter.get(url, ep_params=current_params, headers=headers)
            data = result.data or {}
            pages_fetched += 1
            yield from data.get("value", [])
            next_link = result.next_link
            if not next_link:
                break
            if max_pages is not None and pages_fetched >= max_pages:
                break
            current_params = build_next_params(current_params, next_link)

    def stream(
        self,
        query: ODataQuery | None = None,
        page_size: int | None = None,
        max_pages: int | None = None
    ) -> Generator[T, None, None]:
        """
        Execute the query and yield individual entities, automatically
        fetching next pages until the dataset is exhausted or limits are hit.

        Args:
            query: The ODataQuery options (filter, select, top, etc.).
            page_size: Number of records per HTTP request (B1S-PageSize header).
            max_pages: Safety bound for maximum number of HTTP requests.

        Note:
            ``.top(N)`` here is a **global cap on total rows yielded**, not a page
            size — use ``page_size`` for the per-request batch. ``$top`` is
            enforced client-side and deliberately NOT sent to SAP: forwarding it
            muddles paging (OData re-applies ``$top`` relative to each page's
            ``$skip`` cursor) without changing the row count, so keeping it off
            makes ``.top()`` an unambiguous global cap.

        Yields:
            T: Typed B1Model instances.
        """
        params = query.to_params() if query else {}
        # $top is enforced client-side only (see Note above).
        params.pop("$top", None)
        global_top = query.top if query else None
        headers = {"B1S-PageSize": str(page_size)} if page_size else {}
        yielded_count = 0

        for raw_item in self._iter_pages(self.endpoint, params, headers, max_pages):
            yield self.model.model_validate(raw_item)
            yielded_count += 1
            if global_top is not None and yielded_count >= global_top:
                return

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
            select_fields: list[str] = list(select)
            params["$select"] = ",".join(str(f) for f in select_fields)
        if expand:
            params["$expand"] = _build_expand(expand)

        id_str = format_entity_key(key)
        result = self._adapter.get(f"{self.endpoint}({id_str})", ep_params=params)
        return self.model.model_validate(result.data)

    def exists(self, key: Any) -> bool:
        """Check if an entity exists by attempting to fetch it.
        
        Note: We avoid $select=1 as it's not supported by all SAP SL versions/entities
        and results in 'SAP Error 201: Not supported query string'.
        """
        id_str = format_entity_key(key)
        try:
            self._adapter.get(f"{self.endpoint}({id_str})")
            return True
        except B1NotFoundError:
            return False

    # ── Mutations ─────────────────────────────────────────────────────────────

    def create(self, entity: T) -> T:
        # POST: send all non-None fields. SAP requires a complete payload on creation.
        # model_dump returns native Python bools; re-encode them to tYES/tNO.
        from b1sl.b1sl.models.base import encode_sap_value

        payload = entity.model_dump(exclude_none=True, by_alias=True)
        encoded = {k: encode_sap_value(v) for k, v in payload.items()}
        result = self._adapter.post(f"{self.endpoint}", data=encoded)
        return self.model.model_validate(result.data)

    def update(self, key: Any, entity: T) -> None:
        """PATCH — partial update, SAP SL returns 204 No Content.

        Uses to_api_payload() (exclude_unset) so only fields explicitly set
        by the developer are sent — the correct delta semantics for PATCH.
        Booleans are automatically encoded to tYES/tNO.

        After a successful PATCH, the server-side ETag is guaranteed to have
        changed (a new version was created), but SAP SL returns 204 No Content
        without a new ETag header. The adapter proactively invalidates the
        stale cached ETag on every successful write (PATCH/DELETE/Action), so
        the next mutating call either sends no ETag (blind write) or forces a
        fresh GET first.
        """
        id_str = format_entity_key(key)
        self._adapter.patch(
            f"{self.endpoint}({id_str})",
            data=entity.to_api_payload(),
        )

    def delete(self, key: Any) -> None:
        id_str = format_entity_key(key)
        self._adapter.delete(f"{self.endpoint}({id_str})")

    # ── Actions / Functions ───────────────────────────────────────────────────

    def _action(
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
        """
        id_str = format_entity_key(key)
        url = f"{self.endpoint}({id_str})/{name}"
        if method == "GET":
            result = self._adapter.get(url, ep_params=params, headers=headers)
        else:
            result = self._adapter.post(
                url, ep_params=params, data=payload or {}, headers=headers
            )
        return result.data if result else None

    def _function(self, name: str, params: dict | None = None) -> Any:
        """GET Endpoint/FunctionName(params)"""
        result = self._adapter.get(f"{self.endpoint}/{name}", ep_params=params or {})
        return result.data if result else None
