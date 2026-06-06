# MCP Helpers (`contrib/mcp`)

`b1sl.contrib.mcp` is a framework-agnostic toolkit for building SAP B1 MCP servers.
It covers two surfaces of the SDK:

| Surface | What it helps with |
| :--- | :--- |
| **SQL Queries** | Grammar constraints, tool schemas, result/error formatting |
| **OData resources** | Resource discovery, CRUD tool schemas, entity/collection/error formatting |

No MCP SDK is required or imported. All functions return plain `dict`, `str`, or
dataclasses — plug them into FastMCP, the official MCP Python SDK, or any custom server.

---

## Design principles

- **Grammar knowledge in tool descriptions, not system prompts.** SAP quirks (tYES/tNO,
  date literals, field-name casing) appear in each `inputSchema` parameter description
  so the LLM receives the hint at the moment it needs it.
- **Simple composable tools, not use-case tools.** One primitive per CRUD operation per
  resource (`list`, `get`, `patch`, `create`, `delete`). The agent composes them.
- **Surgical Delta preserved.** PATCH tool descriptions explicitly state "send ONLY the
  fields you explicitly want to change". The SDK's `B1Model.to_api_payload()` enforces
  `exclude_unset=True` under the hood.
- **Elite vs Generic safety signal.** Only the ~28 Elite resources (ETag-safe aliases)
  are registered in the catalog. Non-Elite endpoints require `client.get_resource()` and
  carry no ETag guarantee.

---

## SQL Queries surface

### Grammar constraints

```python
from b1sl.contrib.mcp import (
    SUPPORTED_KEYWORDS,
    SUPPORTED_FUNCTIONS,
    UNSUPPORTED_COMMON,
    sql_grammar_system_prompt,
)

# Opt-in system prompt — embed in your MCP server's system message
print(sql_grammar_system_prompt())
```

`sql_grammar_system_prompt()` is **supplementary grounding only**. The per-tool
`inputSchema` descriptions are the canonical source of grammar hints.

### Tool schemas

```python
from b1sl.contrib.mcp import sql_query_tool_definition

info = client.sql_queries.describe("q_orders")
tool = sql_query_tool_definition(info)
# → {"name": "sql_q_orders", "description": "...", "inputSchema": {...}}
```

### Result and error formatting

```python
from b1sl.contrib.mcp import format_sql_result, format_sql_error

result = client.sql_queries.run("q_orders", cardCode="C001")
text = format_sql_result(result, title="Open Orders")

try:
    client.sql_queries.run("q_orders", wrong_param=1)
except Exception as e:
    text = format_sql_error(e, sql_code="q_orders")
```

---

## OData resources surface

### Resource discovery

```python
from b1sl.contrib.mcp import (
    list_elite_resources,
    resource_descriptor,
    entity_field_catalog,
    ResourceDescriptor,
    FieldDescriptor,
)

# List all 28 Elite aliases
for desc in list_elite_resources():
    print(f"{desc.alias:35s}  {desc.endpoint:35s}  key={desc.key_field}")

# Single resource
desc = resource_descriptor("orders")
# ResourceDescriptor(alias='orders', endpoint='Orders', key_field='DocEntry', ...)

# Introspect a model's fields (no network required)
from b1sl.b1sl import entities as en

fields = entity_field_catalog(en.Document)
scalars = [f for f in fields if not f.is_navigation]
booleans = [f for f in fields if "tYES" in f.type_label]
udfs = [f for f in fields if f.is_udf]
```

`FieldDescriptor` fields: `name` (SAP alias), `python_name`, `type_label`, `required`,
`is_udf`, `is_navigation`. The `@odata.etag` field is always excluded.

### OData grammar prompt

```python
from b1sl.contrib.mcp import odata_query_system_prompt

# Opt-in supplementary grounding for $filter / $select / $orderby / $expand
print(odata_query_system_prompt())
```

### CRUD tool definitions

Build all 5 tools for one resource at once:

```python
from b1sl.contrib.mcp import build_resource_toolset
from b1sl.b1sl import entities as en

tools = build_resource_toolset("orders", en.Document)
# [orders_list, orders_get, orders_patch, orders_create, orders_delete]

for tool in tools:
    mcp_server.register_tool(**tool)
```

Or build individual tools:

```python
from b1sl.contrib.mcp import (
    odata_list_tool_definition,
    odata_get_tool_definition,
    odata_patch_tool_definition,
    odata_create_tool_definition,
    odata_delete_tool_definition,
)

list_tool = odata_list_tool_definition("items", en.Item)
get_tool  = odata_get_tool_definition("items", en.Item)
```

Each tool is self-sufficient — correct use requires no external system prompt.

#### `{alias}_list`

| Parameter | Type | Notes |
| :--- | :--- | :--- |
| `filter` | string | OData `$filter` expression. Booleans: `tYES`/`tNO`. Dates: `/Date(ms)/`. Case-sensitive field names. |
| `select` | string | Comma-separated fields. Always specify — omitting returns 100+ fields. |
| `orderby` | string | e.g. `DocDate desc` |
| `top` | integer | Hard cap on total rows |
| `skip` | integer | Offset pagination |
| `expand` | string | Comma-separated navigation properties |
| `page_size` | integer | Rows per HTTP request |
| `max_pages` | integer | Maximum pages to stream |

All parameters optional — no `required` list.

#### `{alias}_get`

Requires the primary key field (e.g. `DocEntry` for orders, `ItemCode` for items).
Key JSON type is derived from the model: `integer` for DocEntry, `string` for ItemCode/CardCode.
Optional: `select`, `expand`.

#### `{alias}_patch` (Surgical Delta)

Requires only the primary key. All other fields optional. Tool description states:
*"Send ONLY the fields you explicitly want to change — never include fields you did not
explicitly modify (Surgical Delta)."* Navigation fields (e.g. `DocumentLines`) are
included as optional arrays — SAP supports patching document lines in the same request.

#### `{alias}_create`

Required fields derived from `entity_field_catalog` (Pydantic `field_info.is_required()`).
Navigation fields included as optional arrays.

#### `{alias}_delete`

Requires only the primary key. Description warns the operation is irreversible.

### Entity and collection formatting

```python
from b1sl.contrib.mcp import format_entity, format_collection, format_odata_error

# Single entity
item = client.items.get("A001")
text = format_entity(item, title="Item A001")

# Collection (one page from .execute())
page = client.orders.list().filter("DocStatus eq 'bost_Open'").execute()
text = format_collection(page, title="Open Orders", has_more=True)

# Error handling
from b1sl.b1sl.exceptions.exceptions import (
    B1NotFoundError, SAPConcurrencyError, B1ValidationError, B1AuthError,
)

try:
    client.orders.patch(99, en.Document(card_code="NEW"))
except SAPConcurrencyError as e:
    text = format_odata_error(e, resource="orders", key=99)
    # → "Concurrency conflict on orders(99): ETag stale — re-fetch then retry..."
except B1NotFoundError as e:
    text = format_odata_error(e, resource="orders", key=99)
    # → "Record not found with key 99 in 'orders' (HTTP 404)..."
```

`format_entity` separates UDF fields (`U_` prefix) into a dedicated
`### User-Defined Fields` section. Both declared model UDFs and runtime extras
from `model_extra` (SAP returns UDFs not defined in the model schema) are rendered.

`format_odata_error` provides actionable hints per exception type:

| Exception | HTTP | Hint |
| :--- | :--- | :--- |
| `SAPConcurrencyError` | 412 | Re-fetch with GET → re-apply changes → retry PATCH. Not permanent. |
| `B1NotFoundError` | 404 | Verify the primary key and that the record exists. |
| `B1AuthError` | 401 | Session expired — reconnect before retrying. |
| `B1ValidationError` | 400 | Surfaces SAP's field-level message from `details`. |
| `B1ConnectionError` | — | Check network and SAP service availability. |

---

## Building a full MCP server

See `examples/23_mcp_odata_server.py` for a minimal end-to-end server that:

1. Registers CRUD toolsets for every Elite resource.
2. Adds SQL query tools from the catalog.
3. Dispatches tool calls to the SDK.
4. Formats results and errors for LLM context.

---

## Module reference

| Module | Public symbols |
| :--- | :--- |
| `discovery.py` | `ELITE_RESOURCES`, `ResourceDescriptor`, `FieldDescriptor`, `list_elite_resources`, `resource_descriptor`, `entity_field_catalog` |
| `grammar.py` | `SUPPORTED_KEYWORDS`, `SUPPORTED_FUNCTIONS`, `UNSUPPORTED_COMMON`, `sql_grammar_system_prompt` |
| `odata_grammar.py` | `ODATA_OPERATORS`, `ODATA_FUNCTIONS`, `ODATA_SYSTEM_OPTIONS`, `odata_query_system_prompt` |
| `schemas.py` | `sql_query_tool_definition`, `sql_query_input_schema`, `accessible_tables_description` |
| `odata_schemas.py` | `build_resource_toolset`, `odata_list_tool_definition`, `odata_get_tool_definition`, `odata_patch_tool_definition`, `odata_create_tool_definition`, `odata_delete_tool_definition` |
| `formatters.py` | `format_sql_result`, `format_sql_error` |
| `odata_formatters.py` | `format_entity`, `format_collection`, `format_odata_error` |
