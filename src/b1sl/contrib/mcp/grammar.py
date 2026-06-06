"""
b1sl.contrib.mcp.grammar
~~~~~~~~~~~~~~~~~~~~~~~~
SAP Service Layer SQL grammar constraints and LLM prompt helpers.

SAP SL supports only a subset of SQL — LLMs tend to hallucinate unsupported
constructs (CASE WHEN, CTEs, COALESCE, window functions).  Use the constants
and :func:`sql_grammar_system_prompt` to ground any LLM that generates SQL
for the ``SQLQueries`` endpoint.

Typical usage in an MCP server::

    from b1sl.contrib.mcp.grammar import sql_grammar_system_prompt

    system = sql_grammar_system_prompt()
    # Prepend to the LLM system prompt before asking it to write SQL.
    # The model will then avoid generating unsupported constructs.
"""

from __future__ import annotations

SUPPORTED_KEYWORDS: frozenset[str] = frozenset({
    "SELECT", "FROM", "WHERE",
    "AND", "OR", "NOT",
    "BETWEEN", "ORDER BY", "GROUP BY", "HAVING",
    "IS NULL", "IS NOT NULL",
    "LIKE",
    "TOP",
    "UNION", "UNION ALL",
    "IN", "NOT IN",
    "EXISTS",
    "INNER JOIN", "LEFT JOIN", "LEFT OUTER JOIN",
    "RIGHT JOIN", "RIGHT OUTER JOIN",
    "FULL JOIN", "FULL OUTER JOIN",
    "ON", "AS",
    "DISTINCT",
})
"""SQL keywords supported by SAP Service Layer ``SQLQueries``.

This is a subset of standard SQL.  Constructs not in this set are rejected
by SL with a parse error.  See ``UNSUPPORTED_COMMON`` for an explicit list
of constructs that LLMs frequently hallucinate.
"""

SUPPORTED_FUNCTIONS: frozenset[str] = frozenset({
    # Aggregation
    "SUM", "AVG", "MAX", "MIN", "COUNT",
    # Null handling (cross-backend — SL normalizes between HANA and MSSQL)
    "ISNULL", "IFNULL",
    # String
    "LOWER", "UPPER", "LEFT", "RIGHT",
})
"""SQL functions supported by SAP Service Layer ``SQLQueries``.

SL normalizes ``ISNULL`` ↔ ``IFNULL`` between MSSQL and HANA automatically,
so both work regardless of the backend.  Functions not in this set (e.g.
``COALESCE``, ``TRIM``, ``REPLACE``, ``CONCAT``) are not supported.
"""

UNSUPPORTED_COMMON: frozenset[str] = frozenset({
    # Conditionals
    "CASE WHEN",
    "COALESCE",          # use ISNULL / IFNULL instead
    # Type conversions
    "CAST",
    "CONVERT",
    "TRY_CAST",
    "TRY_CONVERT",
    # CTEs
    "WITH",              # Common Table Expressions (WITH ... AS (...))
    # Window / analytic functions
    "OVER",
    "PARTITION BY",
    "ROW_NUMBER",
    "RANK",
    "DENSE_RANK",
    "LAG",
    "LEAD",
    "NTILE",
    # Subquery aliases
    "FROM_SUBQUERY",     # FROM (SELECT ...) AS alias — not supported
    # Aggregated strings
    "STRING_AGG",
    "LISTAGG",
    "GROUP_CONCAT",
    # Date functions
    "DATEADD",
    "DATEDIFF",
    "DATEPART",
    "GETDATE",
    "NOW",
    "SYSDATE",
    # Other common string functions not in the SL list
    "TRIM",
    "LTRIM",
    "RTRIM",
    "REPLACE",
    "SUBSTRING",
    "SUBSTR",
    "CHARINDEX",
    "INSTR",
    "CONCAT",
    "FORMAT",
    "IIF",
    "CHOOSE",
    "PIVOT",
    "UNPIVOT",
    # DML — only SELECT queries are permitted by SQLQueries
    "UPDATE",
    "INSERT",
    "DELETE",
    "ALTER",
    "DROP",
    "CREATE",
    "TRUNCATE",
    "MERGE",
    "EXEC",
    "EXECUTE",
    "CALL",
    "BEGIN",
    "COMMIT",
    "ROLLBACK",
})
"""SQL constructs that are NOT supported by SAP Service Layer.

LLMs frequently generate these.  Use this set to post-validate generated SQL
or to build negative constraints in system prompts.  When ``COALESCE`` is
needed, use ``ISNULL(col, default)`` or ``IFNULL(col, default)`` instead.

DML statements (``UPDATE``, ``INSERT``, ``DELETE``, etc.) are also listed here
because the ``SQLQueries`` endpoint accepts only ``SELECT`` queries — all DML
is rejected with SAP error code 701.
"""


def sql_grammar_system_prompt(*, include_tables: bool = True) -> str:
    """Return a compact system prompt grounding an LLM on SAP SL SQL grammar.

    Prepend this to your LLM system prompt before asking it to generate SQL
    for the ``SQLQueries`` endpoint.  Prevents hallucinations of unsupported
    constructs (CASE WHEN, CTEs, window functions, COALESCE, etc.).

    Args:
        include_tables: When ``True`` (default), appends a brief summary of
            accessible tables and references ``DEFAULT_ACCESSIBLE_TABLES``.
            Set to ``False`` if you are managing table context separately.

    Returns:
        A concise multi-section prompt string optimised for token efficiency.

    Example::

        from b1sl.contrib.mcp.grammar import sql_grammar_system_prompt

        messages = [
            {"role": "system", "content": sql_grammar_system_prompt()},
            {"role": "user", "content": "Write SQL to get all items with OnHand > 0"},
        ]
        # LLM response will use only SL-valid SQL constructs
    """
    sections: list[str] = [
        "## SAP Service Layer SQL constraints",
        "",
        "You are writing SQL for the SAP Service Layer `SQLQueries` endpoint.",
        "This is a restricted SQL dialect — not full ANSI SQL.",
        "",
        "### Supported keywords",
        (
            "SELECT, FROM, WHERE, AND, OR, NOT, BETWEEN … AND, ORDER BY, "
            "GROUP BY, HAVING, IS [NOT] NULL, LIKE, TOP, UNION [ALL], "
            "IN / NOT IN, EXISTS, "
            "INNER JOIN, LEFT [OUTER] JOIN, RIGHT [OUTER] JOIN, FULL [OUTER] JOIN"
        ),
        "",
        "### Supported functions",
        (
            "Aggregation: SUM, AVG, MAX, MIN, COUNT, DISTINCT  "
            "| Null: ISNULL(col, default) or IFNULL(col, default) — both work cross-backend  "
            "| String: LOWER, UPPER, LEFT(col, n), RIGHT(col, n)"
        ),
        "",
        "### NEVER generate these (not supported)",
        (
            "CASE WHEN … END, COALESCE (use ISNULL/IFNULL), "
            "CAST / CONVERT, WITH … AS (CTEs), "
            "window functions (OVER / PARTITION BY / ROW_NUMBER / RANK / LAG / LEAD), "
            "FROM (SELECT …) AS alias (subquery aliases), "
            "TRIM / LTRIM / RTRIM, REPLACE, SUBSTRING, CONCAT, STRING_AGG, "
            "date functions (DATEADD / DATEDIFF / GETDATE / NOW / SYSDATE), "
            "PIVOT / UNPIVOT, IIF, FORMAT"
        ),
        "",
        "### Identifier normalisation (write raw — SL handles it)",
        (
            "- Write unquoted identifiers: `select ItemCode from OITM` "
            "— SL auto-quotes for HANA (`\"ItemCode\"`) and MSSQL (`[ItemCode]`).\n"
            "- Column aliases become JSON response keys — always alias ambiguous columns.\n"
            "- ISNULL and IFNULL are cross-backend equivalents; both are normalised by SL."
        ),
        "",
        "### Parameters",
        (
            "Use `:paramName` placeholders in `SqlText`: "
            "`WHERE \"DocTotal\" > :docTotal`  "
            "Pass values at execution time via `run(code, docTotal=100.0)`."
        ),
        "",
        "### Additional restrictions (all raise error 701 if violated)",
        (
            "- **No `SELECT *`** in the top-level query — use explicit columns.  "
            "`SELECT *` is allowed only inside subqueries "
            "(e.g. `WHERE EXISTS (SELECT * FROM RDR1 t2 ...)`).\n"
            "- **No DML** — only SELECT queries are accepted. "
            "UPDATE, INSERT, DELETE, ALTER, DROP, CREATE, TRUNCATE are all rejected.\n"
            "- **Alias computed columns** — write `SUM(col) AS total`, "
            "never bare `SUM(col)`. Unaliased computed columns are rejected.\n"
            "- **Unique aliases** — no two columns in the same SELECT may share an alias."
        ),
        "",
        "### Security — parameter binding (SQL injection prevention)",
        (
            "**Never interpolate user input into SqlText.** "
            "Always use `:paramName` placeholders and pass values at execution time:\n"
            "  CORRECT: `run('sql01', itemCode=user_value)` "
            "— value is bound server-side by SAP, injection attempts raise error 704.\n"
            "  WRONG:   `sql_text = f\"WHERE ItemCode = '{user_value}'\"` "
            "— bypasses server-side binding and opens injection risk.\n"
            "The Service Layer validates and tokenizes all `ParamList` values; "
            "binding is the only sanctioned way to pass runtime data."
        ),
        "",
        "### Always inaccessible tables (raise error 702 regardless of allowlist)",
        (
            "- **Audit / LOG tables** — tables starting with `A` that mirror a master "
            "table (AITM, ACRD, AINV, AORDR…). Never queryable via SQLQueries.\n"
            "- **SBOCOMMON / SBO-COMMON** — cross-company shared schema. "
            "Always blocked.\n"
            "- **UDT on old tenants** — `@`-prefixed user-defined tables require "
            "SAP B1 10.0 FP 2102 or later."
        ),
    ]

    if include_tables:
        from b1sl.b1sl.resources.sql_queries import _DISPLAY_TABLES_BY_GROUP

        table_lines = ["", "### Accessible tables (default allowlist — partial)"]
        for group, tables in _DISPLAY_TABLES_BY_GROUP.items():
            table_lines.append(f"- **{group}**: {', '.join(tables)}")
        table_lines.append(
            "\nTables outside the allowlist raise error 702. "
            "Full list (200+ tables): `from b1sl.b1sl import DEFAULT_ACCESSIBLE_TABLES`"
        )
        sections.extend(table_lines)

    return "\n".join(sections)
