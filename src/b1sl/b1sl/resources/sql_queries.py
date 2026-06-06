"""
SQLQueries resource — typed wrapper for the SAP Service Layer ``SQLQueries`` endpoint.

Covers the full lifecycle:
- CRUD on stored SQL definitions (via the inherited ``GenericResource`` methods).
- Executing a stored query via the ``/List`` bounded function: ``run()`` / ``run_stream()``.

Usage (sync)::

    sql_queries = client.sql_queries          # Elite alias
    # — or —
    from b1sl.b1sl import entities as en
    sql_queries = client.get_resource(en.SQLQuery, "SQLQueries")

    # One-page result
    result = sql_queries.run("sql04")
    for row in result.rows:
        print(row["ItemCode"])

    # Full paginated stream
    for row in sql_queries.run_stream("sql04", page_size=50):
        process(row)

    # With parameters
    result = sql_queries.run("sql01", docTotal=100.0, docPartner="C001")

Usage (async)::

    async with AsyncB1Client(config) as b1:
        result = await b1.sql_queries.run("sql04")
        async for row in b1.sql_queries.run_stream("sql04", page_size=50):
            await process(row)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, AsyncGenerator, Generator, Type

from b1sl.b1sl.resources.async_base import AsyncGenericResource
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    pass


# ── Allowlist constants ────────────────────────────────────────────────────────

def _build_accessible_tables() -> frozenset[str]:
    tables: set[str] = {
        # Company / Admin
        "CINF", "OADM", "ADM1", "OADP", "OCRN", "OFPR", "OACP",
        "OBPL", "OHLD", "HLD1", "OHFC",
        # Business Partners
        "OCRD", "OCRP", "CRD1", "OCPR",
        # Sales document parents
        "OQUT", "ORDR", "ODLN", "ORRR", "ORDN", "ODPI", "OINV", "ORIN",
        # Purchase document parents
        "OPRQ", "OPQT", "OPOR", "OPDN", "OPRR", "ORPD", "ODPO", "OPCH", "ORPC",
        # Drafts parent
        "ODRF",
        # Payments
        "ORCT", "RCT1", "RCT2", "RCT3", "RCT4",
        "OVPM", "VPM1", "VPM2", "VPM3", "VPM4",
        # Banks
        "ODSC", "DSC1",
        # Items / Inventory
        "OITM", "OITW", "OIBQ", "OBIN", "OBTQ", "OBBQ", "OBTN",
        "OSRQ", "OSBQ", "OSRN",
        # Activities
        "OCLG", "OCLT", "OCLS", "ATC1",
        # Exchange Rates
        "ORTT",
        # Resources
        "ORSC", "RSC1", "RSC2", "RSC3", "RSC4", "RSC5", "RSC6", "ORST",
        # BOM / Production
        "OITT", "ITT1", "ITT2", "OWOR", "WOR1", "WOR4", "ORCJ", "ORCM",
        # Pricing
        "OPLN", "ITM1",
        # GL
        "OJDT", "JDT1",
        # Credit Cards / Deposits
        "OCRC", "OCRH", "ODPS",
        # Electronic Transactions
        "ECM2",
    }
    # Numbered line tables 1-14 for sales, purchase, and drafts doc families
    for prefix in (
        "QUT", "RDR", "DLN", "RRR", "RDN", "DPI", "INV", "RIN",   # sales
        "PRQ", "PQT", "POR", "PDN", "PRR", "RPD", "DPO", "PCH", "RPC",  # purchase
        "DRF",                                                             # drafts
    ):
        for i in range(1, 15):
            tables.add(f"{prefix}{i}")
    return frozenset(tables)


DEFAULT_ACCESSIBLE_TABLES: frozenset[str] = _build_accessible_tables()
"""Frozenset of SAP table names accessible via ``SQLQueries`` by default.

This reflects the default ``b1s_sqltable.conf`` shipped with SAP Service Layer.
Server admins can remove tables (to tighten security) or add tables (outside
SAP support scope).  Use this set to validate SQL before sending it, to hint
users after a 702 error, or to describe MCP tool capabilities.

Tables not in this set will raise ``B1SqlNotAllowedError`` (SAP code 702).

**Always inaccessible (regardless of configuration):**

- **Audit / LOG tables** — tables prefixed with ``A`` that mirror a master table
  (e.g. ``AITM`` for ``OITM``, ``ACRD`` for ``OCRD``).  These exist in the
  database but are explicitly blocked by the Service Layer.
- **SBOCOMMON / SBO-COMMON** — the cross-company shared schema is never
  queryable via this endpoint.
- **User-Defined Tables (UDT)** — supported since SAP B1 10.0 FP 2102; older
  tenants raise 702 for ``@``-prefixed tables.
"""

KNOWN_INACCESSIBLE_PATTERNS = {
    "log_tables": (
        "Tables prefixed with 'A' that are audit logs of master tables "
        "(AITM, ACRD, AINV, etc.) — blocked regardless of b1s_sqltable.conf."
    ),
    "sbocommon": (
        "SBOCOMMON / SBO-COMMON cross-company schema — never queryable via SQLQueries."
    ),
    "udt_old_tenants": (
        "User-Defined Tables (@-prefixed) on tenants older than SAP B1 10.0 FP 2102."
    ),
}
"""Documented patterns that are always inaccessible via ``SQLQueries``.

These are not in ``DEFAULT_ACCESSIBLE_TABLES`` and cannot be added via server
configuration.  Use this dict to produce better 702 error messages when the
table name matches one of these patterns.
"""

_DISPLAY_TABLES_BY_GROUP = {
    "Items / Inventory": ["OITM", "OITW", "OIBQ", "OBIN", "OBTN"],
    "Sales": ["ORDR", "OINV", "ODLN", "OQUT"],
    "Purchase": ["OPOR", "OPCH", "OPDN", "OPRQ"],
    "Business Partners": ["OCRD", "OCRP", "CRD1", "OCPR"],
    "Payments": ["ORCT", "OVPM"],
    "GL": ["OJDT", "JDT1"],
    "Production": ["OWOR", "OITT"],
    "Pricing": ["OPLN", "ITM1"],
    "Activities": ["OCLG"],
    "Company / Admin": ["CINF", "OADM", "OBPL"],
}


# ── Query metadata ─────────────────────────────────────────────────────────────

@dataclass
class SQLQueryInfo:
    """Structured metadata for a stored SQLQuery entity.

    Returned by :meth:`SQLQueriesResource.describe` and its async counterpart.
    Use this to validate parameters before calling :meth:`run`, or to generate
    MCP tool schemas via :mod:`b1sl.contrib.mcp`.

    Attributes:
        sql_code: The primary key (``SqlCode``) used to address the query.
        sql_name: Human-readable name stored alongside the SQL.
        sql_text: The SQL text as normalized by SAP on the last save.
        params: Ordered list of named parameter identifiers parsed from
            ``ParamList`` (e.g. ``["docTotal", "cardCode"]``).  Empty when
            the query has no parameters.
    """

    sql_code: str
    sql_name: str | None
    sql_text: str | None
    params: list[str]


# ── Parameter serialization ────────────────────────────────────────────────────

def _format_sql_params(params: dict[str, Any]) -> str:
    """Serialize keyword arguments to SAP's ``ParamList`` string format.

    SAP expects a ``&``-separated string where string values are enclosed in
    single quotes and numeric / boolean values are bare::

        docTotal=100.0&docPartner='C001'&active=1

    Rules:
    - ``str``  → value is single-quoted; internal ``'`` is escaped as ``''``.
    - ``bool`` → ``1`` (True) or ``0`` (False).  Must check before ``int``
                 because ``bool`` is a subclass of ``int`` in Python.
    - ``int`` / ``float`` → bare numeric string.
    - Everything else → ``str()`` conversion, then single-quoted.

    **SQL injection safety**: the Service Layer validates and tokenizes parameter
    values on the server side — injection attempts (e.g. ``value='; DROP TABLE``
    embedded in a param value) are rejected with SAP error 704.  However, this
    protection applies *only* to parameter values passed through this function.
    Never interpolate user-supplied data directly into ``SqlText`` using f-strings
    or ``str.format()`` — always pass user input as ``**params`` to ``run()`` so
    the binding goes through the ``ParamList`` mechanism.

    Note: The param *names* must match exactly (case-sensitive) the named
    parameters declared in ``SqlText`` (e.g. ``:docTotal``).  SAP returns a
    generic ``"704 Parameter error."`` without naming the offending parameter.

    Note on storage vs invocation format:
    - ``ParamList`` stored on the entity uses ``,`` as separator: ``"a,b,c"``.
    - ``ParamList`` used in ``/List`` POST body uses ``&``: ``"a=1&b='x'"``.
    These are two different semantics for the same field name.
    """
    parts: list[str] = []
    for name, value in params.items():
        if isinstance(value, bool):
            parts.append(f"{name}={1 if value else 0}")
        elif isinstance(value, (int, float)):
            parts.append(f"{name}={value}")
        else:
            escaped = str(value).replace("'", "''")
            parts.append(f"{name}='{escaped}'")
    return "&".join(parts)


# ── Result container ───────────────────────────────────────────────────────────

@dataclass
class SQLRunResult:
    """Result of a single-page ``/List`` execution.

    Attributes:
        rows: The query result rows.  Each dict maps column aliases (exactly
            as written in the ``SELECT`` clause) to their values.  The schema
            is dynamic — it depends on the SQL stored in SAP.
        sql_text: The normalized SQL that SAP actually executed (useful for
            debugging — SAP rewrites identifiers for the backend).
        next_link: The raw ``@odata.nextLink`` value if more pages exist,
            ``None`` otherwise.  Use ``run_stream()`` instead of managing
            pagination manually.
        raw: The full parsed JSON response body from SAP.
    """

    rows: list[dict[str, Any]] = field(default_factory=list)
    sql_text: str = ""
    next_link: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)

    def __iter__(self):
        return iter(self.rows)

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, index: int) -> dict[str, Any]:
        return self.rows[index]

    @property
    def has_more(self) -> bool:
        """True when SAP returned a nextLink — more pages are available."""
        return self.next_link is not None

    def to_pydantic(self, model: Type[Any]) -> list[Any]:
        """Validate and convert ``rows`` into a list of Pydantic model instances.

        Useful when the SQL SELECT shape is known and the caller wants typed
        access with IDE autocomplete::

            class ItemRow(BaseModel):
                ItemCode: str
                ItemName: str

            result = client.sql_queries.run("sql04")
            typed_rows = result.to_pydantic(ItemRow)
            print(typed_rows[0].ItemCode)

        Args:
            model: A Pydantic ``BaseModel`` subclass whose fields match the
                column aliases in the ``SELECT`` clause.

        Returns:
            List of validated model instances.
        """
        return [model.model_validate(row) for row in self.rows]

    @classmethod
    def _from_raw(cls, data: dict[str, Any]) -> "SQLRunResult":
        next_link = data.get("@odata.nextLink") or data.get("odata.nextLink")
        return cls(
            rows=data.get("value", []),
            sql_text=data.get("SqlText", ""),
            next_link=next_link,
            raw=data,
        )


# ── Sync resource ──────────────────────────────────────────────────────────────

class SQLQueriesResource(GenericResource["SQLQuery"]):
    """Sync resource for the SAP ``SQLQueries`` endpoint.

    Inherits full CRUD from ``GenericResource``:
    - ``get(code)`` / ``list()`` / ``stream()`` — read definitions.
    - ``create(entity)`` / ``update(code, entity)`` / ``delete(code)`` — manage definitions.

    Adds SQL execution:
    - ``run(code, **params)`` — execute and return first page as ``SQLRunResult``.
    - ``run_stream(code, **params)`` — execute and stream all rows across pages.
    """

    endpoint = "SQLQueries"

    def __init__(self, adapter):
        from b1sl.b1sl.models._generated.entities.general import SQLQuery
        self.model = SQLQuery
        super().__init__(adapter)

    def run(
        self,
        code: str,
        *,
        page_size: int | None = None,
        method: str = "POST",
        **params: Any,
    ) -> SQLRunResult:
        """Execute a stored SQL query and return the first page of results.

        Args:
            code: The ``SqlCode`` key of the stored ``SQLQuery`` entity.
            page_size: Override the server default page size (sent as
                ``Prefer: odata.maxpagesize=N`` header).  Default is the
                server default (20 rows on most tenants).
            method: ``"POST"`` (default) or ``"GET"``.  POST is preferred
                because it avoids URL-length limits and keeps parameters
                out of server logs.
            **params: Named parameters matching the ``:name`` placeholders
                in the stored ``SqlText``.  Names are case-sensitive.

        Returns:
            ``SQLRunResult`` with ``.rows``, ``.sql_text``, ``.next_link``.
            Check ``.has_more`` or use ``run_stream()`` for full datasets.

        Raises:
            B1SqlNotAllowedError: SAP codes 702/703 — table or column blocked.
            B1SqlParamError: SAP code 704 — missing, extra, or mis-typed param.
            B1NotFoundError: The ``SqlCode`` does not exist.
        """
        headers: dict[str, str] = {}
        if page_size is not None:
            headers["Prefer"] = f"odata.maxpagesize={page_size}"

        payload = {"ParamList": _format_sql_params(params)} if params else None

        from b1sl.b1sl.exceptions.exceptions import B1SqlParamError
        try:
            data = self._action(
                code,
                "List",
                payload=payload,
                headers=headers if headers else None,
                method=method,
                params=params if method == "GET" and params else None,
            )
        except B1SqlParamError as exc:
            if exc.expected_params is None:
                try:
                    exc.expected_params = self.describe(code).params
                except Exception:
                    pass
            raise
        return SQLRunResult._from_raw(data or {})

    def describe(self, code: str) -> SQLQueryInfo:
        """Return structured metadata for a stored SQL query.

        Fetches the ``SQLQuery`` entity and parses ``ParamList`` into an
        ordered list of parameter names.  Use this to validate kwargs before
        calling :meth:`run`, or to generate MCP tool schemas.

        Args:
            code: The ``SqlCode`` of the stored ``SQLQuery`` entity.

        Returns:
            :class:`SQLQueryInfo` with ``sql_code``, ``sql_name``,
            ``sql_text``, and ``params`` (empty list when no params).

        Raises:
            B1NotFoundError: When the ``SqlCode`` does not exist.
        """
        entity = self.get(code)
        raw = entity.param_list or ""
        params_list = [p.strip() for p in raw.split(",") if p.strip()]
        return SQLQueryInfo(
            sql_code=entity.sql_code or code,
            sql_name=entity.sql_name,
            sql_text=entity.sql_text,
            params=params_list,
        )

    def run_stream(
        self,
        code: str,
        *,
        page_size: int | None = None,
        max_pages: int | None = None,
        **params: Any,
    ) -> Generator[dict[str, Any], None, None]:
        """Execute a stored SQL query and stream all rows across pages.

        Follows ``@odata.nextLink`` automatically until the dataset is exhausted
        or ``max_pages`` is reached.  Always uses POST to avoid URL-length issues
        with large parameter sets.

        Args:
            code: The ``SqlCode`` key of the stored ``SQLQuery`` entity.
            page_size: Rows per HTTP request (``Prefer: odata.maxpagesize=N``).
            max_pages: Safety ceiling on the number of HTTP requests.
            **params: Named parameters for the stored SQL.

        Yields:
            Raw row dicts.  Keys are the column aliases from the ``SELECT``.
        """
        headers: dict[str, str] = {}
        if page_size is not None:
            headers["Prefer"] = f"odata.maxpagesize={page_size}"

        # First page via POST with body
        payload = {"ParamList": _format_sql_params(params)} if params else None
        first_data = self._action(code, "List", payload=payload, headers=headers or None)
        first_data = first_data or {}
        yield from first_data.get("value", [])

        next_link = first_data.get("@odata.nextLink") or first_data.get("odata.nextLink")
        if not next_link:
            return

        # Subsequent pages via GET (nextLink is always GET-based)
        from b1sl.b1sl.pagination import build_next_params
        pages_fetched = 1
        current_params: dict[str, Any] = {}
        if params:
            current_params["ParamList"] = _format_sql_params(params)

        while next_link:
            if max_pages is not None and pages_fetched >= max_pages:
                break
            current_params = build_next_params(current_params, next_link)
            page_data = self._action(
                code, "List", method="GET", params=current_params, headers=headers or None
            )
            page_data = page_data or {}
            yield from page_data.get("value", [])
            pages_fetched += 1
            next_link = page_data.get("@odata.nextLink") or page_data.get("odata.nextLink")


# ── Async resource ─────────────────────────────────────────────────────────────

class AsyncSQLQueriesResource(AsyncGenericResource["SQLQuery"]):
    """Async resource for the SAP ``SQLQueries`` endpoint.

    Mirrors ``SQLQueriesResource`` with async/await semantics.
    """

    endpoint = "SQLQueries"

    def __init__(self, adapter):
        from b1sl.b1sl.models._generated.entities.general import SQLQuery
        self.model = SQLQuery
        super().__init__(adapter)

    async def describe(self, code: str) -> SQLQueryInfo:
        """Async variant of :meth:`SQLQueriesResource.describe`.

        Args:
            code: The ``SqlCode`` of the stored ``SQLQuery`` entity.

        Returns:
            :class:`SQLQueryInfo` with parsed parameter list.

        Raises:
            B1NotFoundError: When the ``SqlCode`` does not exist.
        """
        entity = await self.get(code)
        raw = entity.param_list or ""
        params_list = [p.strip() for p in raw.split(",") if p.strip()]
        return SQLQueryInfo(
            sql_code=entity.sql_code or code,
            sql_name=entity.sql_name,
            sql_text=entity.sql_text,
            params=params_list,
        )

    async def run(
        self,
        code: str,
        *,
        page_size: int | None = None,
        method: str = "POST",
        **params: Any,
    ) -> SQLRunResult:
        """Execute a stored SQL query and return the first page of results.

        See ``SQLQueriesResource.run`` for full parameter documentation.
        """
        headers: dict[str, str] = {}
        if page_size is not None:
            headers["Prefer"] = f"odata.maxpagesize={page_size}"

        payload = {"ParamList": _format_sql_params(params)} if params else None

        from b1sl.b1sl.exceptions.exceptions import B1SqlParamError
        try:
            data = await self._action(
                code,
                "List",
                payload=payload,
                headers=headers if headers else None,
                method=method,
                params=params if method == "GET" and params else None,
            )
        except B1SqlParamError as exc:
            if exc.expected_params is None:
                try:
                    exc.expected_params = (await self.describe(code)).params
                except Exception:
                    pass
            raise
        return SQLRunResult._from_raw(data or {})

    async def run_stream(
        self,
        code: str,
        *,
        page_size: int | None = None,
        max_pages: int | None = None,
        **params: Any,
    ) -> AsyncGenerator[dict[str, Any], None]:
        """Execute a stored SQL query and stream all rows across pages.

        See ``SQLQueriesResource.run_stream`` for full parameter documentation.
        """
        headers: dict[str, str] = {}
        if page_size is not None:
            headers["Prefer"] = f"odata.maxpagesize={page_size}"

        payload = {"ParamList": _format_sql_params(params)} if params else None
        first_data = await self._action(code, "List", payload=payload, headers=headers or None)
        first_data = first_data or {}
        for item in first_data.get("value", []):
            yield item

        next_link = first_data.get("@odata.nextLink") or first_data.get("odata.nextLink")
        if not next_link:
            return

        from b1sl.b1sl.pagination import build_next_params
        pages_fetched = 1
        current_params: dict[str, Any] = {}
        if params:
            current_params["ParamList"] = _format_sql_params(params)

        while next_link:
            if max_pages is not None and pages_fetched >= max_pages:
                break
            current_params = build_next_params(current_params, next_link)
            page_data = await self._action(
                code, "List", method="GET", params=current_params, headers=headers or None
            )
            page_data = page_data or {}
            for item in page_data.get("value", []):
                yield item
            pages_fetched += 1
            next_link = page_data.get("@odata.nextLink") or page_data.get("odata.nextLink")
