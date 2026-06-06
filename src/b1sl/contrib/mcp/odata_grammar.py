"""
b1sl.contrib.mcp.odata_grammar
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SAP Service Layer OData query grammar constants and LLM prompt helpers.

SAP B1 SL implements a hybrid OData v3/v4 dialect with several quirks that
LLMs tend to get wrong (boolean encoding, date literals, field-name casing).
Use the constants and :func:`odata_query_system_prompt` to ground any LLM
that generates OData queries for the Service Layer.

Typical usage in an MCP server::

    from b1sl.contrib.mcp.odata_grammar import odata_query_system_prompt

    system = odata_query_system_prompt()
    # Prepend to the LLM system prompt before asking it to filter entities.
"""

from __future__ import annotations

ODATA_OPERATORS: frozenset[str] = frozenset({
    "eq",
    "ne",
    "gt",
    "ge",
    "lt",
    "le",
    "and",
    "or",
    "not",
})
"""OData logical and comparison operators supported by SAP Service Layer.

All operators are lowercase keywords separated by spaces:
``FieldName eq 'value'``, ``Amount gt 100``, ``(A eq 1) and (B ne 2)``.
"""

ODATA_FUNCTIONS: frozenset[str] = frozenset({
    "contains",
    "startswith",
    "endswith",
    "substringof",
})
"""String-predicate functions that SAP Service Layer honours in ``$filter``.

- ``contains(FieldName, 'text')``   — OData v4 style; preferred.
- ``startswith(FieldName, 'text')`` — OData v4 style.
- ``endswith(FieldName, 'text')``   — OData v4 style.
- ``substringof('text', FieldName)`` — OData v3 style; note reversed argument
  order compared to the v4 functions above. SAP SL accepts both styles.

Do NOT use ``indexof``, ``substring``, ``tolower``, ``toupper``, ``trim``,
``concat``, ``length`` — they are not reliably supported by SAP SL.
"""

ODATA_SYSTEM_OPTIONS: frozenset[str] = frozenset({
    "$filter",
    "$select",
    "$orderby",
    "$expand",
    "$top",
    "$skip",
    "$count",
    "$inlinecount",
    "$apply",
})
"""OData system query options supported by SAP Service Layer.

``$count`` returns the total number of matching entities (added to URL as
``$count=true``). ``$inlinecount=allpages`` is the OData v3 equivalent;
value must be ``allpages`` or ``none`` — any other value returns 400.
``$skip`` combined with ``$top`` enables manual pagination
(though ``odata.nextLink`` / ``@odata.nextLink`` is the preferred mechanism).
``$apply`` enables server-side aggregation (SAP HANA only, B1 9.1 patch 12+).
"""


def odata_query_system_prompt() -> str:
    """Return a compact system prompt grounding an LLM on SAP OData query syntax.

    Covers the $filter / $select / $expand / $orderby grammar, SAP-specific
    encoding quirks (booleans, dates, enums), and the $select discipline.

    Returns:
        A concise multi-section prompt string optimised for token efficiency.

    Example::

        from b1sl.contrib.mcp.odata_grammar import odata_query_system_prompt

        messages = [
            {"role": "system", "content": odata_query_system_prompt()},
            {"role": "user", "content": "List open sales orders for BP C001"},
        ]
    """
    sections: list[str] = [
        "## SAP Service Layer OData query constraints",
        "",
        "You are building OData queries for the SAP Business One Service Layer.",
        "SL implements a hybrid OData v3/v4 dialect with several SAP-specific rules.",
        "",
        "### Comparison operators (all lowercase, space-separated)",
        (
            "``eq``  ``ne``  ``gt``  ``ge``  ``lt``  ``le``  "
            "``and``  ``or``  ``not``\n"
            "Example: ``$filter=DocTotal gt 500 and DocStatus eq 'O'``"
        ),
        "",
        "### String functions in $filter",
        (
            "- ``contains(FieldName, 'text')`` — preferred (OData v4)\n"
            "- ``startswith(FieldName, 'text')``\n"
            "- ``endswith(FieldName, 'text')``\n"
            "- ``substringof('text', FieldName)`` — OData v3 style; "
            "**note argument order is reversed** compared to contains/startswith/endswith\n"
            "Do NOT use: ``indexof``, ``substring``, ``tolower``, ``toupper``, "
            "``trim``, ``concat``, ``length``"
        ),
        "",
        "### Boolean fields — tYES / tNO encoding",
        (
            "SAP B1 encodes boolean fields as the **string** ``'tYES'`` or ``'tNO'``, "
            "NOT as ``true`` or ``false``.\n"
            "CORRECT:  ``$filter=Frozen eq 'tNO'``\n"
            "WRONG:    ``$filter=Frozen eq false``\n"
            "This applies to every boolean-style field across all entities "
            "(items, business partners, orders, etc.)."
        ),
        "",
        "### Date fields — multiple formats accepted",
        (
            "SAP SL accepts several date literal formats in ``$filter``:\n"
            "- ISO string: ``'2014-04-23'`` or compact ``'20140423'``\n"
            "- With ``datetime`` prefix: ``datetime'2014-04-23'`` or "
            "``datetime'20140423'``\n"
            "- With time component (time is ignored): ``'2014-04-23T12:21:21'`` "
            "or ``'20140423000000'``\n"
            "**SAP B1 ignores HOUR/MINUTE/SECOND parts for date-type fields.**\n"
            "Example: ``$filter=DocDate ge '2024-01-01' and DocDate lt '2024-04-01'``\n"
            "In responses, dates appear as ``\"/Date(1704067200000)/\"`` — "
            "divide by 1000 to get Unix seconds."
        ),
        "",
        "### Time fields (DocTime and similar)",
        (
            "SAP SL time fields accept these formats in ``$filter``:\n"
            "``'18:38:00'``, ``'18:38'``, ``'183800'``, ``'1838'``, or ISO with "
            "date prefix: ``'2014-06-18T18:38:00Z'``.\n"
            "**SAP B1 ignores YEAR/MONTH/DAY parts; only HOUR/MINUTE are effective.**\n"
            "Example: ``$filter=DocTime ge '09:00'``"
        ),
        "",
        "### String quoting, escaping, and null",
        (
            "String literals are enclosed in **single quotes**: ``'value'``.\n"
            "To include a single quote inside a string, double it: ``'O''Reilly'``.\n"
            "Null/missing values: ``ForeignName eq null`` (no quotes around ``null``).\n"
            "Field names are **case-sensitive** — use the exact casing from the "
            "entity schema (e.g. ``ItemCode``, not ``itemcode`` or ``ITEMCODE``)."
        ),
        "",
        "### Enum fields — value or name both accepted",
        (
            "SAP SL accepts both the enum *value* (short code) and the enum *name* "
            "(full identifier) in ``$filter``:\n"
            "- ``CardType eq 'C'``         — enum value (customer)\n"
            "- ``CardType eq 'cCustomer'`` — enum name (equivalent)\n"
            "Common examples:\n"
            "- Document status: ``DocStatus eq 'O'`` (open) or ``'C'`` (closed)\n"
            "- Item type: ``ItemType eq 'itItems'`` or ``'itLabor'``\n"
            "Valid values are defined on each entity type — never guess numeric codes."
        ),
        "",
        "### $select discipline — always project explicit fields",
        (
            "**Always include a $select clause** listing only the fields you need.\n"
            "Omitting $select returns the full entity payload (~100+ fields for "
            "Orders), which wastes bandwidth and LLM context.\n"
            "CORRECT: ``$select=DocEntry,CardCode,DocTotal,DocStatus``\n"
            "WRONG:   (no $select) — returns every field on the entity"
        ),
        "",
        "### $expand for navigation properties",
        (
            "Use ``$expand`` to include related collections inline:\n"
            "``$expand=DocumentLines`` — includes line items in the response.\n"
            "Multiple expansions: ``$expand=DocumentLines,DocumentAdditionalExpenses``\n"
            "Navigation property names are PascalCase and entity-specific.\n"
            "\n"
            "**Nested ``$select`` inside ``$expand`` (B1 10.0 FP 2105+):**\n"
            "Scope which fields each expanded navigation returns:\n"
            "``$expand=BusinessPartner($select=CardCode,ContactPerson),"
            "Item($select=ItemCode,ItemName)&$select=Subject``\n"
            "Equivalent via cross-navigation paths in ``$select``:\n"
            "``$expand=BusinessPartner,Item"
            "&$select=BusinessPartner/CardCode,BusinessPartner/ContactPerson,"
            "Item/ItemCode,Item/ItemName,Subject``\n"
            "The SDK dict form ``expand={'BusinessPartner': ['CardCode', 'ContactPerson']}`` "
            "generates the nested ``$select`` syntax automatically."
        ),
        "",
        "### $orderby",
        (
            "``$orderby=FieldName asc`` or ``$orderby=FieldName desc``\n"
            "Multiple fields: ``$orderby=CardCode asc,DocDate desc``"
        ),
        "",
        "### Aggregation and grouping ($apply) — SAP HANA only",
        (
            "``$apply`` enables server-side aggregation and grouping "
            "(B1 9.1 patch 12+ for aggregation; B1 9.2 PL03+ for groupby).\n"
            "\n"
            "**Aggregate syntax** — ``$apply=aggregate(FieldName with method as Alias)``\n"
            "Supported methods: "
            "``sum``, ``avg``/``average``, ``min``, ``max``, "
            "``countdistinct``/``distinctcount``.\n"
            "Row count via virtual property: ``aggregate($count as OrdersCount)`` "
            "(no ``with`` keyword).\n"
            "**The alias (``as Alias``) is required on every expression.**\n"
            "Examples:\n"
            "- ``$apply=aggregate(DocRate with sum as TotalDocRate)``\n"
            "- ``$apply=aggregate($count as OrdersCount)``\n"
            "Result: single-row ``value`` array with only the aliased property.\n"
            "\n"
            "**Groupby (simple)** — ``$apply=groupby((Field1, Field2))``\n"
            "Equivalent to SQL ``GROUP BY``. "
            "Example: ``$apply=groupby((CardCode, DocStatus))``\n"
            "\n"
            "**Groupby with aggregation:**\n"
            "``$apply=groupby((CardCode), aggregate(DocNum with sum as TotalDocNum))``\n"
            "\n"
            "**Chained transforms — filter before groupby (separated by /):**\n"
            "``$apply=filter(Orders/CardCode eq 'c001')"
            "/groupby((CardCode), aggregate(DocNum with sum as TotalDocNum))``\n"
            "The ``filter()`` transform inside ``$apply`` uses "
            "``EntityName/FieldName`` navigation paths. "
            "Alternatively, ``&$filter=...`` after ``$apply`` is functionally equivalent."
        ),
        "",
        "### Cross-joins ($crossjoin) — SAP HANA only, B1 9.2 patch 07+",
        (
            "``$crossjoin`` queries across entity sets with no predefined navigation.\n"
            "Path: ``/b1s/v1/$crossjoin(Entity1,Entity2)``\n"
            "**A bare ``$crossjoin`` without ``$expand``/``$filter`` returns 400 "
            "— always include a join condition and field projection.**\n"
            "\n"
            "Typical pattern:\n"
            "``$crossjoin(Orders,BusinessPartners)"
            "?$expand=Orders($select=DocEntry,DocNum)"
            ",BusinessPartners($select=CardCode)"
            "&$filter=Orders/CardCode eq BusinessPartners/CardCode``\n"
            "\n"
            "Navigation paths in ``$crossjoin`` always use "
            "``EntityName/FieldName`` syntax: "
            "``Orders/CardCode``, ``BusinessPartners/CardCode``.\n"
            "\n"
            "**Arithmetic in ``$expand`` (calculated columns):** "
            "``Orders($select=DocEntry mul (DocNum sub 1) as DocSeq)``\n"
            "Supported operations: ``add``, ``sub``, ``mul``, ``div``.\n"
            "\n"
            "**Cross-join with aggregation** — chain ``filter()/groupby()`` via ``$apply``:\n"
            "``$apply=filter(Orders/CardCode eq BusinessPartners/CardCode)"
            "/groupby((BusinessPartners/CardCode),"
            "aggregate(Orders(DocNum with max as MaxDocNum)))``"
        ),
        "",
        "### Pagination and $inlinecount",
        (
            "Use ``$top`` and ``$skip`` for manual paging, or follow the "
            "``@odata.nextLink`` / ``odata.nextLink`` URL in the response.\n"
            "**When ``$top`` and ``$skip`` are combined, ``$skip`` is applied "
            "first regardless of their order in the URL.**\n"
            "The Service Layer also respects ``Prefer: odata.maxpagesize=N`` "
            "to control server-side page size.\n"
            "**``$inlinecount=allpages``** adds the total matching count to the "
            "response as ``\"odata.count\": \"N\"`` — useful when the result spans "
            "multiple pages and you need the grand total, not just the page count. "
            "Valid values are ``allpages`` or ``none`` (or omit); any other value "
            "returns 400 Bad Request."
        ),
        "",
        "### Row-level filter via QueryService_PostQuery (SAP HANA only, B1 9.2 PL11+)",
        (
            "Joins a document header with its navigation lines for row-level filtering.\n"
            "Use when you need to filter by line-level fields (ItemCode, LineNum, etc.) "
            "combined with header fields — which regular ``$filter`` cannot do.\n"
            "\n"
            "**POST** ``/b1s/v1/QueryService_PostQuery`` with JSON body:\n"
            "``{\"QueryPath\": \"$crossjoin(Orders,Orders/DocumentLines)\","
            " \"QueryOption\": \"$expand=...&$filter=...\"}``\n"
            "\n"
            "The ``QueryPath`` supports navigation paths: "
            "``$crossjoin(Orders,Orders/DocumentLines)``.\n"
            "``QueryOption`` is the OData query string (``$expand``, ``$filter``, "
            "``$apply``, ``$orderby``, ``$top``, ``$skip``) joined with ``&``.\n"
            "\n"
            "Example — filter on header + lines:\n"
            "QueryPath: ``$crossjoin(Orders,Orders/DocumentLines)``\n"
            "QueryOption: "
            "``$expand=Orders($select=DocEntry,DocNum),"
            "Orders/DocumentLines($select=ItemCode,LineNum)"
            "&$filter=Orders/DocEntry eq Orders/DocumentLines/DocEntry"
            " and Orders/DocumentLines/ItemCode eq 'WIDGET'``\n"
            "\n"
            "Navigation paths always use ``Entity/NavProperty/FieldName`` syntax.\n"
            "Response content-type is ``text/plain`` but contains valid JSON. "
            "``odata.nextLink`` pagination is not supported — use ``$top``/``$skip``."
        ),
        "",
        "### System query options summary",
        (
            "``$filter``  ``$select``  ``$orderby``  ``$expand``  "
            "``$top``  ``$skip``  ``$count``  ``$inlinecount``  ``$apply``"
        ),
    ]
    return "\n".join(sections)
