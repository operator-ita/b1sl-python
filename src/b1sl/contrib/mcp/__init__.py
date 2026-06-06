"""
b1sl.contrib.mcp
~~~~~~~~~~~~~~~~
Generic MCP helper utilities for building SAP B1 MCP servers.

This package provides framework-agnostic building blocks — pure Python
dicts, strings, and dataclasses — that can be plugged into any MCP server
implementation (FastMCP, the official MCP Python SDK, custom servers, etc.).

No MCP SDK dependency is required or imported.

Typical usage::

    from b1sl.contrib.mcp import sql_query_tool_definition, format_sql_result

    info = client.sql_queries.describe("sql04")

    # Build a tool definition for your MCP server
    tool_def = sql_query_tool_definition(info)
    # → {"name": "sql_sql04", "description": "...", "inputSchema": {...}}

    # Format results for LLM context
    result = client.sql_queries.run("sql04")
    text = format_sql_result(result)
    # → markdown table string
"""

from b1sl.contrib.mcp.discovery import (
    ELITE_RESOURCES,
    FieldDescriptor,
    ResourceDescriptor,
    entity_field_catalog,
    list_elite_resources,
    resource_descriptor,
)
from b1sl.contrib.mcp.formatters import format_sql_error, format_sql_result
from b1sl.contrib.mcp.grammar import (
    SUPPORTED_FUNCTIONS,
    SUPPORTED_KEYWORDS,
    UNSUPPORTED_COMMON,
    sql_grammar_system_prompt,
)
from b1sl.contrib.mcp.odata_formatters import (
    format_collection,
    format_entity,
    format_odata_error,
)
from b1sl.contrib.mcp.odata_grammar import (
    ODATA_FUNCTIONS,
    ODATA_OPERATORS,
    ODATA_SYSTEM_OPTIONS,
    odata_query_system_prompt,
)
from b1sl.contrib.mcp.odata_schemas import (
    build_resource_toolset,
    odata_create_tool_definition,
    odata_crossjoin_tool_definition,
    odata_delete_tool_definition,
    odata_get_tool_definition,
    odata_list_tool_definition,
    odata_patch_tool_definition,
    query_service_tool_definition,
)
from b1sl.contrib.mcp.schemas import (
    accessible_tables_description,
    sql_query_input_schema,
    sql_query_tool_definition,
)

__all__ = [
    # OData resource discovery
    "ELITE_RESOURCES",
    "ResourceDescriptor",
    "FieldDescriptor",
    "list_elite_resources",
    "resource_descriptor",
    "entity_field_catalog",
    # SQL grammar constraints
    "SUPPORTED_KEYWORDS",
    "SUPPORTED_FUNCTIONS",
    "UNSUPPORTED_COMMON",
    "sql_grammar_system_prompt",
    # OData grammar constraints
    "ODATA_OPERATORS",
    "ODATA_FUNCTIONS",
    "ODATA_SYSTEM_OPTIONS",
    "odata_query_system_prompt",
    # OData CRUD tool definitions
    "odata_list_tool_definition",
    "odata_get_tool_definition",
    "odata_patch_tool_definition",
    "odata_create_tool_definition",
    "odata_delete_tool_definition",
    "build_resource_toolset",
    "odata_crossjoin_tool_definition",
    "query_service_tool_definition",
    # SQL tool schemas
    "accessible_tables_description",
    "sql_query_input_schema",
    "sql_query_tool_definition",
    # Result / error formatting — SQL
    "format_sql_result",
    "format_sql_error",
    # Result / error formatting — OData
    "format_entity",
    "format_collection",
    "format_odata_error",
]
