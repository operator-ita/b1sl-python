"""
b1sl.contrib.mcp.formatters
~~~~~~~~~~~~~~~~~~~~~~~~~~~
MCP response formatters for b1sl SQL query results and errors.

All functions return plain strings (MCP TextContent value).
No MCP SDK dependency — wrap the output in whatever content type your server uses.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from b1sl.b1sl.resources.sql_queries import SQLQueryInfo, SQLRunResult


def format_sql_result(
    result: "SQLRunResult",
    *,
    max_rows: int = 50,
    title: str | None = None,
) -> str:
    """Format a ``SQLRunResult`` as markdown text suitable for LLM context.

    Produces a markdown table with column headers derived from the first row.
    Truncated rows are noted at the bottom.

    Args:
        result: The ``SQLRunResult`` from ``client.sql_queries.run()``.
        max_rows: Maximum rows to include in the table.  Rows beyond this are
            summarized as a footnote rather than omitted silently.
        title: Optional H2 heading inserted before the table.

    Returns:
        Markdown-formatted string ready for MCP ``TextContent``.

    Example::

        result = client.sql_queries.run("sql04")
        text = format_sql_result(result, title="Items on Hand")
        # → "## Items on Hand\\n| ItemCode | OnHand |\\n..."
    """
    lines: list[str] = []

    if title:
        lines.append(f"## {title}\n")

    rows_to_show = result.rows[:max_rows]
    truncated = len(result.rows) - len(rows_to_show)

    if not rows_to_show:
        lines.append("*No rows returned.*")
        return "\n".join(lines)

    headers = list(rows_to_show[0].keys())
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows_to_show:
        cells = [str(row.get(h, "")) for h in headers]
        lines.append("| " + " | ".join(cells) + " |")

    footnotes: list[str] = []
    if truncated:
        footnotes.append(f"*{truncated} row(s) omitted (max_rows={max_rows})*")
    if result.has_more:
        footnotes.append(
            "*More pages available — use `run_stream()` for the full dataset.*"
        )
    if footnotes:
        lines.append("\n" + "  ".join(footnotes))

    return "\n".join(lines)


def format_sql_error(
    exc: Exception,
    *,
    sql_code: str | None = None,
    describe_result: "SQLQueryInfo | None" = None,
) -> str:
    """Format a b1sl SQL exception as a diagnostic message for LLMs.

    Provides actionable hints based on the error type.  When ``describe_result``
    or ``exc.expected_params`` is available, the message lists the parameter
    names expected by the query so the agent can self-correct.

    Args:
        exc: The caught exception (``B1SqlNotAllowedError``, ``B1SqlParamError``,
            or any ``B1Exception`` subclass).
        sql_code: The ``SqlCode`` that was executed (adds context to the message).
        describe_result: ``SQLQueryInfo`` from ``describe()`` — used to hint
            expected parameters on a 704 error when ``exc.expected_params`` is
            not already set.

    Returns:
        Plain text error message suitable for MCP error content or tool output.

    Example::

        try:
            result = client.sql_queries.run("sql04", wrong_param=1)
        except B1SqlParamError as e:
            msg = format_sql_error(e, sql_code="sql04")
            # → "SQL parameter error (query: 'sql04'): ...\\n→ Expected parameters: :docTotal"
    """
    from b1sl.b1sl.exceptions.exceptions import (
        B1NotFoundError,
        B1SqlNotAllowedError,
        B1SqlParamError,
        B1SqlSyntaxError,
    )

    ctx = f" (query: {sql_code!r})" if sql_code else ""

    if isinstance(exc, B1SqlSyntaxError):
        return (
            f"SQL syntax error{ctx}: SAP rejected the SQL as invalid (error 701).\n"
            "Common causes:\n"
            "  • SELECT * in the main query — use explicit column names "
            "(SELECT * is only allowed inside subqueries)\n"
            "  • Unsupported function — e.g. LENGTH, CASE WHEN, COALESCE, CAST "
            "(see grammar.UNSUPPORTED_COMMON for the full list)\n"
            "  • DML statement — UPDATE/INSERT/DELETE/ALTER are not permitted; "
            "only SELECT queries are accepted\n"
            "  • Duplicate alias — two columns sharing the same alias\n"
            "  • Computed column without alias — write SUM(col) AS total, "
            "not bare SUM(col)\n"
            f"SAP message: {exc}"
        )

    if isinstance(exc, B1SqlNotAllowedError):
        if exc.sap_code == "702":
            from b1sl.b1sl.resources.sql_queries import _DISPLAY_TABLES_BY_GROUP
            groups = "; ".join(
                f"{group}: {', '.join(tables)}"
                for group, tables in _DISPLAY_TABLES_BY_GROUP.items()
            )
            msg_body = str(exc)
            extra_hint = ""
            # SBOCOMMON is unambiguously documented as permanently inaccessible
            if "SBOCOMMON" in msg_body or "SBO-COMMON" in msg_body:
                extra_hint = (
                    "\n→ SBOCOMMON / SBO-COMMON is never queryable via SQLQueries."
                )
            return (
                f"SQL execution blocked{ctx}: the queried table is not in the SAP "
                "Service Layer allowlist (b1s_sqltable.conf). "
                "This cannot be fixed at runtime — the server configuration must change.\n"
                f"Accessible tables by default — {groups}. "
                "Full list: b1sl.DEFAULT_ACCESSIBLE_TABLES. "
                f"Error [{exc.sap_code}]: {exc}"
                + extra_hint
            )
        # code 703
        return (
            f"SQL execution blocked{ctx}: a queried column is in the SAP "
            "ColumnExcludeList. Update the SQL to avoid that column, or request "
            f"the server configuration change. Error [{exc.sap_code}]: {exc}"
        )

    if isinstance(exc, B1SqlParamError):
        msg = f"SQL parameter error{ctx}: {exc}"
        expected = getattr(exc, "expected_params", None)
        if not expected and describe_result is not None:
            expected = describe_result.params
        if expected:
            formatted = ", ".join(f":{p}" for p in expected)
            msg += (
                f"\n→ Expected parameters: {formatted}"
                "\n→ Parameter names are case-sensitive and must match the "
                ":name placeholders in SqlText exactly."
            )
        return msg

    if isinstance(exc, B1NotFoundError):
        return (
            f"SQL query{ctx} not found in SAP — verify the SqlCode exists. "
            f"Error: {exc}"
        )

    return f"SQL query error{ctx}: {exc}"
