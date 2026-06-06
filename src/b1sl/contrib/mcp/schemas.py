"""
b1sl.contrib.mcp.schemas
~~~~~~~~~~~~~~~~~~~~~~~~
JSON Schema generators for SAP B1 SQL query MCP tools.

All functions return plain Python dicts compatible with the MCP Tool spec
(https://spec.modelcontextprotocol.io/specification/server/tools/).
No MCP SDK import is required — plug the output into any MCP framework.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from b1sl.b1sl.resources.sql_queries import SQLQueryInfo


def sql_query_input_schema(params: list[str]) -> dict:
    """Build a JSON Schema for a SQLQuery ``/List`` invocation.

    Covers the SQL named parameters plus optional pagination controls
    (``page_size``, ``max_pages``).  Pass as ``inputSchema`` in an MCP tool.

    Args:
        params: Ordered list of parameter names (from ``SQLQueryInfo.params``).
            Pass an empty list for queries that take no parameters.

    Returns:
        JSON Schema dict ready to use as MCP tool ``inputSchema``.

    Example::

        info = client.sql_queries.describe("sql04")
        schema = sql_query_input_schema(info.params)
        # → {"type": "object", "properties": {...}, "required": [...]}
    """
    properties: dict = {
        "page_size": {
            "type": "integer",
            "description": (
                "Rows per HTTP request (Prefer: odata.maxpagesize=N). "
                "Default: server setting (~20 rows). "
                "Use with max_pages to cap total rows fetched."
            ),
        },
        "max_pages": {
            "type": "integer",
            "description": (
                "Maximum number of pages to fetch when streaming. "
                "Omit when using run() for a single-page result."
            ),
        },
    }
    required: list[str] = []

    for name in params:
        properties[name] = {
            "type": ["string", "number", "boolean"],
            "description": (
                f"SQL parameter :{name}. "
                "Case-sensitive — must match the :name placeholder in SqlText exactly. "
                "Strings are auto-quoted; numbers and booleans are passed bare."
            ),
        }
        required.append(name)

    schema: dict = {"type": "object", "properties": properties}
    if required:
        schema["required"] = required
    return schema


def accessible_tables_description() -> str:
    """Return a compact human-readable summary of SAP's default table allowlist.

    Use this in MCP tool or resource descriptions to inform agents which tables
    they can query via ``SQLQueries`` without hitting a 702 error.

    Returns:
        A multi-line markdown string grouping accessible tables by category.

    Example::

        @mcp_tool(description="Run stored SQL. " + accessible_tables_description())
        async def run_sql(code: str) -> str: ...
    """
    from b1sl.b1sl.resources.sql_queries import _DISPLAY_TABLES_BY_GROUP

    lines = ["**Accessible SAP tables (default allowlist):**"]
    for group, tables in _DISPLAY_TABLES_BY_GROUP.items():
        lines.append(f"- **{group}**: {', '.join(tables)} (+ line tables)")
    lines.append(
        "\nFull list (200+ tables including line tables): "
        "`from b1sl.b1sl import DEFAULT_ACCESSIBLE_TABLES`"
    )
    return "\n".join(lines)


def sql_query_tool_definition(info: "SQLQueryInfo") -> dict:
    """Build a complete MCP Tool definition dict from a ``SQLQueryInfo``.

    The returned dict has the shape expected by the MCP specification::

        {
            "name": str,          # "sql_<sql_code>" — valid identifier
            "description": str,   # includes param hints and SQL snippet
            "inputSchema": dict,  # JSON Schema
        }

    Plug the result into your MCP server's tool registry.  The ``name``
    uses the ``SqlCode`` prefixed with ``sql_`` (hyphens and dots replaced
    with underscores to ensure a valid identifier).

    Args:
        info: ``SQLQueryInfo`` returned by ``client.sql_queries.describe(code)``.

    Returns:
        MCP-compatible tool definition dict.

    Example::

        info = client.sql_queries.describe("sql04")
        tool = sql_query_tool_definition(info)
        # → {
        #       "name": "sql_sql04",
        #       "description": "Run stored SQL query 'queryOnItem'. ...",
        #       "inputSchema": {"type": "object", ...}
        #   }
    """
    safe_code = info.sql_code.replace("-", "_").replace(".", "_")
    tool_name = f"sql_{safe_code}"

    param_hint = ""
    if info.params:
        formatted = ", ".join(f":{p}" for p in info.params)
        param_hint = f" Parameters: {formatted}."

    display_name = info.sql_name or info.sql_code
    description = f"Run stored SQL query '{display_name}'.{param_hint}"

    if info.sql_text:
        snippet = info.sql_text[:120].replace("\n", " ")
        ellipsis = "..." if len(info.sql_text) > 120 else ""
        description += f" SQL: {snippet}{ellipsis}"

    return {
        "name": tool_name,
        "description": description,
        "inputSchema": sql_query_input_schema(info.params),
    }
