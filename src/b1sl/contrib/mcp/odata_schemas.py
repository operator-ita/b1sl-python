"""
b1sl.contrib.mcp.odata_schemas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MCP tool-definition builders for SAP B1 OData CRUD operations.

All functions return plain Python dicts compatible with the MCP Tool spec.
No MCP SDK import required — plug the output into any MCP framework.

Each tool is self-sufficient: grammar knowledge (tYES/tNO, field-name casing,
$select discipline) lives inline in each ``inputSchema`` parameter description
so the LLM receives the hint at the moment it needs it.

Typical usage::

    from b1sl.contrib.mcp.odata_schemas import build_resource_toolset
    from b1sl.b1sl import entities as en

    tools = build_resource_toolset("orders", en.Document)
    # → [orders_list, orders_get, orders_patch, orders_create, orders_delete]
    for tool in tools:
        mcp_server.register_tool(**tool)
"""

from __future__ import annotations

from b1sl.contrib.mcp.discovery import entity_field_catalog, resource_descriptor

# ── Internal helpers ──────────────────────────────────────────────────────────

def _json_type(type_label: str) -> dict:
    """Map a FieldDescriptor.type_label to a JSON Schema type fragment."""
    if type_label == "integer":
        return {"type": "integer"}
    if type_label == "number":
        return {"type": "number"}
    if type_label.startswith("boolean"):
        # Boolean fields are passed as Python bool in PATCH/CREATE payloads;
        # the SDK's B1Model converts to tYES/tNO before sending to SAP.
        return {"type": "boolean"}
    if type_label == "collection":
        return {"type": "array", "items": {"type": "object"}}
    if type_label == "object":
        return {"type": "object"}
    return {"type": "string"}


def _key_json_type(key_field: str, fields: list) -> str:
    """Return 'integer' or 'string' for the primary key field."""
    for f in fields:
        if f.name == key_field:
            return "integer" if f.type_label == "integer" else "string"
    return "string"


# ── Public tool-definition builders ──────────────────────────────────────────

def odata_list_tool_definition(alias: str, model: type) -> dict:
    """Build an MCP tool definition for listing and filtering an Elite resource.

    Generates a ``{alias}_list`` tool with OData query parameters ($filter,
    $select, $orderby, $expand, $top, $skip) and pagination controls.

    Grammar knowledge is embedded inline in each parameter description:
    tYES/tNO boolean encoding, field-name case-sensitivity, $select discipline.

    Args:
        alias: Elite resource alias (e.g. ``"orders"``).
        model: B1Model subclass for the resource (used for $select example).

    Returns:
        MCP-compatible tool definition dict with ``name``, ``description``,
        and ``inputSchema`` keys.

    Example::

        from b1sl.b1sl import entities as en
        tool = odata_list_tool_definition("orders", en.Document)
        mcp_server.register_tool(**tool)
    """
    desc = resource_descriptor(alias)
    fields = entity_field_catalog(model)
    scalar_names = [f.name for f in fields if not f.is_navigation]
    sample = ", ".join(scalar_names[:5]) if scalar_names else desc.key_field

    return {
        "name": f"{alias}_list",
        "description": (
            f"List and filter {desc.description}. "
            "Returns a paginated collection. "
            "Always specify $select — omitting it returns 100+ fields and wastes context."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "filter": {
                    "type": "string",
                    "description": (
                        "OData $filter expression. "
                        "Examples: \"CardCode eq 'C001'\", \"DocTotal gt 1000\", "
                        "\"contains(ItemName, 'widget')\". "
                        "Booleans: tYES / tNO (e.g. \"Frozen eq 'tNO'\"). "
                        "Dates: ISO string '2024-01-01' or datetime'2024-01-01' "
                        "(SAP ignores time parts for date fields). "
                        "Time fields: '18:38' or '183800'. "
                        "Null check: \"ForeignName eq null\" (no quotes around null). "
                        "Enums accept short value ('C') or full name ('cCustomer'). "
                        "Field names are case-sensitive (PascalCase as in SAP). "
                        "String values require single quotes."
                    ),
                },
                "select": {
                    "type": "string",
                    "description": (
                        "Comma-separated field names for $select. "
                        "ALWAYS specify explicit fields — omitting $select returns "
                        "100+ fields and wastes context. "
                        f"Example: \"{sample}\"."
                    ),
                },
                "orderby": {
                    "type": "string",
                    "description": (
                        "OData $orderby clause. Example: \"DocDate desc\". "
                        "Field names are case-sensitive."
                    ),
                },
                "top": {
                    "type": "integer",
                    "description": (
                        "Total rows to return ($top, a hard cap). The SDK eager-fills "
                        "up to N across server pages; use instead of page_size/max_pages "
                        "for a bounded result."
                    ),
                },
                "skip": {
                    "type": "integer",
                    "description": "Skip the first N rows ($skip). Use for offset pagination.",
                },
                "expand": {
                    "type": "string",
                    "description": (
                        "Comma-separated navigation properties to inline via $expand. "
                        "Example: \"DocumentLines,BillToAddress\". "
                        "Each expanded collection multiplies response size."
                    ),
                },
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
                        "Omit to fetch a single page."
                    ),
                },
                "apply": {
                    "type": "string",
                    "description": (
                        "OData $apply expression (SAP HANA only). "
                        "Aggregation (B1 9.1 patch 12+): "
                        "\"aggregate(FieldName with method as Alias)\". "
                        "Methods: sum, avg/average, min, max, countdistinct. "
                        "Row count: \"aggregate($count as Total)\". "
                        "Groupby (B1 9.2 PL03+): \"groupby((Field1, Field2))\". "
                        "Groupby + aggregate: "
                        "\"groupby((CardCode), aggregate(DocNum with sum as Total))\". "
                        "Chained filter: "
                        "\"filter(Field eq 'v')/groupby((Field), aggregate(...))\". "
                        "The alias (as Alias) is required in every aggregate expression."
                    ),
                },
            },
        },
    }


def odata_get_tool_definition(alias: str, model: type) -> dict:
    """Build an MCP tool definition for fetching a single entity by primary key.

    Args:
        alias: Elite resource alias (e.g. ``"orders"``).
        model: B1Model subclass for the resource.

    Returns:
        MCP-compatible tool definition dict.

    Example::

        from b1sl.b1sl import entities as en
        tool = odata_get_tool_definition("items", en.Item)
    """
    desc = resource_descriptor(alias)
    key_field = desc.key_field
    fields = entity_field_catalog(model)
    kt = _key_json_type(key_field, fields)

    return {
        "name": f"{alias}_get",
        "description": (
            f"Fetch a single {desc.description.rstrip('.')} by {key_field}. "
            "Use $select to limit returned fields and avoid retrieving 100+ fields."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                key_field: {
                    "type": kt,
                    "description": (
                        f"Primary key ({key_field}) identifying the "
                        f"{desc.endpoint} record."
                    ),
                },
                "select": {
                    "type": "string",
                    "description": (
                        "Comma-separated $select fields. "
                        "ALWAYS specify — omitting returns 100+ fields and wastes context."
                    ),
                },
                "expand": {
                    "type": "string",
                    "description": (
                        "Comma-separated $expand navigation properties. "
                        "Example: \"DocumentLines\"."
                    ),
                },
            },
            "required": [key_field],
        },
    }


def odata_patch_tool_definition(alias: str, model: type) -> dict:
    """Build an MCP tool definition for partially updating an entity (Surgical Delta).

    The Surgical Delta pattern is enforced via the tool description: only fields
    explicitly set by the caller should be included in the PATCH payload.  The
    SDK's ``B1Model.to_api_payload()`` already implements this via
    ``exclude_unset=True`` — this tool definition makes the constraint explicit
    to the LLM at the moment of invocation.

    Args:
        alias: Elite resource alias (e.g. ``"orders"``).
        model: B1Model subclass for the resource.

    Returns:
        MCP-compatible tool definition dict.

    Example::

        from b1sl.b1sl import entities as en
        tool = odata_patch_tool_definition("business_partners", en.BusinessPartner)
    """
    desc = resource_descriptor(alias)
    key_field = desc.key_field
    fields = entity_field_catalog(model)
    kt = _key_json_type(key_field, fields)

    properties: dict = {
        key_field: {
            "type": kt,
            "description": (
                f"Primary key ({key_field}) of the {desc.endpoint} record to update."
            ),
        }
    }

    for f in fields:
        if f.name == key_field:
            continue
        if f.is_navigation:
            prop: dict = {
                **_json_type(f.type_label),
                "description": (
                    f"Navigation property {f.name} ($expand target). "
                    "Include only to replace nested records in this PATCH."
                ),
            }
        else:
            udf_note = " (UDF)" if f.is_udf else ""
            prop = {
                **_json_type(f.type_label),
                "description": f"{f.name} field to update.{udf_note}",
            }
        properties[f.name] = prop

    return {
        "name": f"{alias}_patch",
        "description": (
            f"Partially update a {desc.description.rstrip('.')} (PATCH). "
            "Send ONLY the fields you explicitly want to change — never include "
            "fields you did not explicitly modify (Surgical Delta). "
            "ETag concurrency is enforced: fetch the entity first to obtain the current ETag."
        ),
        "inputSchema": {
            "type": "object",
            "properties": properties,
            "required": [key_field],
        },
    }


def odata_create_tool_definition(alias: str, model: type) -> dict:
    """Build an MCP tool definition for creating a new entity.

    Required vs optional fields are derived from ``entity_field_catalog``:
    fields with no default value appear in ``inputSchema.required``.

    Args:
        alias: Elite resource alias (e.g. ``"orders"``).
        model: B1Model subclass for the resource.

    Returns:
        MCP-compatible tool definition dict.

    Example::

        from b1sl.b1sl import entities as en
        tool = odata_create_tool_definition("orders", en.Document)
    """
    desc = resource_descriptor(alias)
    fields = entity_field_catalog(model)

    properties: dict = {}
    required: list[str] = []

    for f in fields:
        if f.is_navigation:
            prop: dict = {
                **_json_type(f.type_label),
                "description": (
                    f"Navigation property {f.name}. "
                    "Pass an array of objects for nested records (e.g. document lines)."
                ),
            }
        else:
            udf_note = " (UDF)" if f.is_udf else ""
            prop = {
                **_json_type(f.type_label),
                "description": f"{f.name} field.{udf_note}",
            }
        properties[f.name] = prop
        if f.required:
            required.append(f.name)

    input_schema: dict = {"type": "object", "properties": properties}
    if required:
        input_schema["required"] = required

    return {
        "name": f"{alias}_create",
        "description": (
            f"Create a new {desc.description.rstrip('.')}. "
            f"Returns the created entity with its assigned {desc.key_field}. "
            "Required fields are listed in inputSchema.required."
        ),
        "inputSchema": input_schema,
    }


def odata_delete_tool_definition(alias: str, model: type) -> dict:
    """Build an MCP tool definition for deleting an entity by primary key.

    Args:
        alias: Elite resource alias (e.g. ``"orders"``).
        model: B1Model subclass for the resource.

    Returns:
        MCP-compatible tool definition dict.

    Example::

        from b1sl.b1sl import entities as en
        tool = odata_delete_tool_definition("orders", en.Document)
    """
    desc = resource_descriptor(alias)
    key_field = desc.key_field
    fields = entity_field_catalog(model)
    kt = _key_json_type(key_field, fields)

    return {
        "name": f"{alias}_delete",
        "description": (
            f"Delete a {desc.description.rstrip('.')} by {key_field}. "
            "This operation is irreversible. "
            "ETag concurrency is enforced: fetch the entity first to lock the current version."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                key_field: {
                    "type": kt,
                    "description": (
                        f"Primary key ({key_field}) of the "
                        f"{desc.endpoint} record to delete."
                    ),
                },
            },
            "required": [key_field],
        },
    }


def query_service_tool_definition() -> dict:
    """Build an MCP tool definition for ``QueryService_PostQuery`` (row-level filter).

    Generates a ``query_service`` tool for joining document headers with their
    navigation lines via POST.  Essential for filtering by line-level fields
    (ItemCode, LineNum, Quantity, etc.) combined with header fields.

    Returns:
        MCP-compatible tool definition dict with ``name``, ``description``,
        and ``inputSchema`` keys.

    Example::

        tool = query_service_tool_definition()
        mcp_server.register_tool(**tool)
    """
    return {
        "name": "query_service",
        "description": (
            "Filter document lines combined with header fields via QueryService_PostQuery "
            "(SAP HANA only, B1 9.2 PL11+). "
            "Use when you need to filter by line-level fields (ItemCode, LineNum, Quantity) "
            "together with header fields — which regular $filter on a single entity cannot do. "
            "Sends a POST request with QueryPath and QueryOption in the body. "
            "Requires at least expand or apply — omitting both returns 400."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query_path": {
                    "type": "string",
                    "description": (
                        "The QueryPath for the POST body. "
                        "Typically a crossjoin including a navigation path: "
                        "\"$crossjoin(Orders,Orders/DocumentLines)\". "
                        "Supports navigation paths (Entity/NavProperty) and "
                        "multi-entity joins: \"$crossjoin(Orders,Orders/DocumentLines,BusinessPartners)\". "
                        "Entity and navigation names are case-sensitive PascalCase."
                    ),
                },
                "expand": {
                    "type": "object",
                    "description": (
                        "Per-entity field projections as a JSON object. "
                        "Keys are entity names or navigation paths; values are field lists. "
                        "Example: {\"Orders\": [\"DocEntry\", \"DocNum\"], "
                        "\"Orders/DocumentLines\": [\"ItemCode\", \"LineNum\"]}. "
                        "ALWAYS specify expand or apply — bare query returns 400."
                    ),
                    "additionalProperties": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                "filter": {
                    "type": "string",
                    "description": (
                        "OData $filter expression. "
                        "Navigation paths use Entity/NavProperty/FieldName syntax: "
                        "\"Orders/DocEntry eq Orders/DocumentLines/DocEntry "
                        "and Orders/DocumentLines/ItemCode eq 'WIDGET'\". "
                        "String literals in single quotes; null without quotes."
                    ),
                },
                "apply": {
                    "type": "string",
                    "description": (
                        "OData $apply for aggregation/groupby (alternative to expand). "
                        "Example: \"filter(Orders/DocEntry eq Orders/DocumentLines/DocEntry)"
                        "/groupby((Orders/DocNum),aggregate(Orders/DocumentLines($count as Lines)))\". "
                        "Use apply instead of expand when you need aggregated results."
                    ),
                },
                "orderby": {
                    "type": "string",
                    "description": (
                        "OData $orderby using navigation paths. "
                        "Example: \"Orders/DocNum desc\"."
                    ),
                },
                "top": {
                    "type": "integer",
                    "description": (
                        "Hard cap on total rows ($top). "
                        "Use for manual paging — QueryService does not support odata.nextLink."
                    ),
                },
                "skip": {
                    "type": "integer",
                    "description": (
                        "Skip the first N rows ($skip). "
                        "Combine with top for manual paging."
                    ),
                },
            },
            "required": ["query_path"],
        },
    }


def odata_crossjoin_tool_definition() -> dict:
    """Build an MCP tool definition for ``$crossjoin`` queries.

    Cross-joins query across entity sets with no predefined navigation
    (SAP HANA only, B1 9.2 patch 07+).  The tool name is ``crossjoin`` —
    a single generic tool rather than a per-resource variant, because the
    entities are specified as arguments by the LLM.

    Returns:
        MCP-compatible tool definition dict with ``name``, ``description``,
        and ``inputSchema`` keys.

    Example::

        tool = odata_crossjoin_tool_definition()
        mcp_server.register_tool(**tool)
    """
    return {
        "name": "crossjoin",
        "description": (
            "Execute a $crossjoin query across SAP B1 entity sets that have no "
            "predefined navigation relationship (SAP HANA only, B1 9.2 patch 07+). "
            "A bare crossjoin without expand or apply returns 400 — always provide "
            "at least one of: expand (for field projection) or apply (for aggregation). "
            "Navigation paths use EntityName/FieldName syntax throughout "
            "(e.g. 'Orders/CardCode eq BusinessPartners/CardCode'). "
            "Results are plain dicts — no entity model applies."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "entities": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 2,
                    "description": (
                        "Two or more SAP B1 entity set names to cross-join. "
                        "Use the exact PascalCase endpoint name "
                        "(e.g. ['Orders', 'BusinessPartners'] or "
                        "['Orders', 'BusinessPartners', 'Activities']). "
                        "Entity names are case-sensitive."
                    ),
                },
                "expand": {
                    "type": "object",
                    "description": (
                        "Per-entity field projections as a JSON object. "
                        "Keys are entity names; values are lists of field names. "
                        "Example: {\"Orders\": [\"DocEntry\", \"DocNum\"], "
                        "\"BusinessPartners\": [\"CardCode\", \"CardName\"]}. "
                        "Arithmetic in select (add/sub/mul/div): "
                        "pass the expression verbatim as a string in the list, "
                        "e.g. \"DocEntry mul (DocNum sub 1) as DocSeq\". "
                        "ALWAYS specify expand or apply — bare crossjoin returns 400."
                    ),
                    "additionalProperties": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                "filter": {
                    "type": "string",
                    "description": (
                        "OData $filter applied after the crossjoin. "
                        "Navigation paths use EntityName/FieldName syntax: "
                        "\"Orders/CardCode eq BusinessPartners/CardCode\". "
                        "Supports standard OData functions: "
                        "contains, startswith, endswith. "
                        "String literals in single quotes; "
                        "null without quotes: \"ForeignName eq null\"."
                    ),
                },
                "apply": {
                    "type": "string",
                    "description": (
                        "OData $apply expression for server-side aggregation "
                        "(SAP HANA only, B1 9.2 PL03+). "
                        "Chain filter + groupby: "
                        "\"filter(Orders/CardCode eq BusinessPartners/CardCode)"
                        "/groupby((BusinessPartners/CardCode),"
                        "aggregate(Orders(DocNum with max as MaxDocNum)))\". "
                        "Methods: sum, avg, min, max, countdistinct, $count. "
                        "The alias (as Alias) is required in every aggregate. "
                        "Use apply instead of expand when you need aggregated results."
                    ),
                },
                "orderby": {
                    "type": "string",
                    "description": (
                        "OData $orderby clause. "
                        "Use EntityName/FieldName paths: \"Orders/DocNum desc\". "
                        "Multiple fields: \"BusinessPartners/CardCode asc, Orders/DocNum desc\"."
                    ),
                },
                "top": {
                    "type": "integer",
                    "description": "Hard cap on total rows returned ($top).",
                },
                "skip": {
                    "type": "integer",
                    "description": "Skip the first N rows ($skip). $skip is applied before $top.",
                },
            },
            "required": ["entities"],
        },
    }


def build_resource_toolset(
    alias: str, model: type, *, read_only: bool = False
) -> list[dict]:
    """Build the CRUD tool definitions for an Elite resource.

    Returns one tool per operation in registration order:
    ``list``, ``get``, ``patch``, ``create``, ``delete`` — or only the two
    read tools when ``read_only=True``.

    Exposing write tools grants the connected LLM create/update/delete on the
    resource; the grammar system prompts are advisory only, so deployers who
    do not need writes should pass ``read_only=True`` (and those who do are
    encouraged to pair writes with ``client.dry_run()`` or a confirmation
    layer).

    Args:
        alias: Elite resource alias (e.g. ``"orders"``).
        model: B1Model subclass for the resource.
        read_only: When True, omit the ``patch``/``create``/``delete`` tools.

    Returns:
        List of MCP-compatible tool definition dicts (5, or 2 if read-only).

    Example::

        from b1sl.b1sl import entities as en
        tools = build_resource_toolset("orders", en.Document, read_only=True)
        for tool in tools:
            mcp_server.register_tool(**tool)
    """
    tools = [
        odata_list_tool_definition(alias, model),
        odata_get_tool_definition(alias, model),
    ]
    if not read_only:
        tools.extend([
            odata_patch_tool_definition(alias, model),
            odata_create_tool_definition(alias, model),
            odata_delete_tool_definition(alias, model),
        ])
    return tools
