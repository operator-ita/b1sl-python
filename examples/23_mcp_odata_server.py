"""
Example 23: MCP OData Server — full CRUD toolset for Elite resources

Demonstrates how to use ``b1sl.contrib.mcp`` to build a framework-agnostic
MCP server that exposes the full OData surface of the SAP B1 SDK:

- Auto-register CRUD toolsets (list/get/patch/create/delete) for every Elite resource.
- Dispatch incoming tool calls to the appropriate SDK method.
- Format results and errors as markdown text for LLM context.
- Add SQL query tools alongside OData tools.

This example uses a simple hand-rolled dispatcher — no MCP SDK required.
Swap the dispatcher for FastMCP, the official MCP Python SDK, or any other
framework that accepts ``{"name", "description", "inputSchema"}`` tool dicts.

Prerequisites:
    B1SL_BASE_URL, B1SL_USERNAME, B1SL_PASSWORD, B1SL_COMPANY_DB env vars
    (or a populated .env file at the project root).
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from b1sl.b1sl import B1Client, B1Environment
from b1sl.b1sl import entities as en
from b1sl.b1sl.exceptions.exceptions import B1Exception
from b1sl.b1sl.resources.odata import QueryBuilder
from b1sl.contrib.mcp import (
    build_resource_toolset,
    format_collection,
    format_entity,
    format_odata_error,
    list_elite_resources,
    odata_crossjoin_tool_definition,
    odata_query_system_prompt,
    query_service_tool_definition,
    resource_descriptor,
)

# ── Helpers ───────────────────────────────────────────────────────────────────

def section(title: str) -> None:
    print(f"\n{'─' * 70}")
    print(f"  {title}")
    print(f"{'─' * 70}")


# ── Tool registry ─────────────────────────────────────────────────────────────
#
# Maps each alias to its Pydantic model so build_resource_toolset can derive
# the correct field types, key field JSON type, and required list.
#
# In a real server you would enumerate ALL Elite resources; here we register a
# representative subset to keep the example concise.

_ALIAS_TO_MODEL: dict[str, type] = {
    "items":             en.Item,
    "business_partners": en.BusinessPartner,
    "orders":            en.Document,
    "invoices":          en.Document,
    "purchase_orders":   en.Document,
}

# Build and print the toolset so the example is runnable without a live SAP system
def build_tool_registry() -> dict[str, dict]:
    """Return a flat {tool_name: tool_def} registry from all registered aliases."""
    registry: dict[str, dict] = {}
    for alias, model in _ALIAS_TO_MODEL.items():
        for tool in build_resource_toolset(alias, model):
            registry[tool["name"]] = tool
    # Cross-join is entity-agnostic — one shared tool for all entity pairs
    cj_tool = odata_crossjoin_tool_definition()
    registry[cj_tool["name"]] = cj_tool
    # QueryService (POST row-level filter) — one shared tool
    qs_tool = query_service_tool_definition()
    registry[qs_tool["name"]] = qs_tool
    return registry


# ── Dispatcher ────────────────────────────────────────────────────────────────
#
# A minimal dispatcher that maps "{alias}_{verb}" tool calls to SDK methods.
# Replace this with your MCP framework's handler registration in production.

def dispatch_tool_call(
    client: B1Client,
    tool_name: str,
    args: dict[str, Any],
) -> str:
    """Execute a registered OData tool call and return formatted markdown."""
    # Parse alias and verb from the tool name (e.g. "orders_list" → "orders", "list")
    parts = tool_name.rsplit("_", 1)
    if len(parts) != 2:
        return f"Unknown tool: {tool_name!r}"
    alias, verb = parts[0], parts[1]

    try:
        desc = resource_descriptor(alias)
    except KeyError as e:
        return str(e)

    # Elite aliases are direct client properties (e.g. client.orders, client.items)
    resource = getattr(client, alias)
    key_field = desc.key_field

    try:
        if verb == "list":
            qb = QueryBuilder(resource)
            if args.get("filter"):
                qb = qb.filter(args["filter"])
            if args.get("select"):
                qb = qb.select(args["select"])
            if args.get("orderby"):
                qb = qb.orderby(args["orderby"])
            if args.get("top"):
                qb = qb.top(args["top"])
            if args.get("skip"):
                qb = qb.skip(args["skip"])
            if args.get("expand"):
                qb = qb.expand(args["expand"])
            if args.get("apply"):
                qb = qb.apply(args["apply"])
            if args.get("page_size") or args.get("max_pages"):
                # Streaming mode: follow nextLink across pages, bounded by max_pages.
                rows = list(qb.stream(
                    page_size=args.get("page_size"),
                    max_pages=args.get("max_pages"),
                ))
                return format_collection(rows, title=f"{alias} list")
            # Single-page mode: PaginatedResult knows whether more pages exist.
            page = qb.execute()
            return format_collection(
                page, title=f"{alias} list", has_more=page.has_more
            )

        elif verb == "get":
            key = args[key_field]
            model = resource.get(key)
            return format_entity(model, title=f"{alias}({key})")

        elif verb == "patch":
            key = args.pop(key_field)
            model_cls = _ALIAS_TO_MODEL[alias]
            payload = model_cls(**{k: v for k, v in args.items()})
            resource.update(key, payload)
            return f"PATCH {alias}({key}) — updated successfully."

        elif verb == "create":
            model_cls = _ALIAS_TO_MODEL[alias]
            payload = model_cls(**args)
            created = resource.create(payload)
            key = getattr(created, key_field.lower(), "?")
            return f"CREATE {alias} — created with {key_field}={key}."

        elif verb == "delete":
            key = args[key_field]
            resource.delete(key)
            return f"DELETE {alias}({key}) — deleted successfully."

        else:
            return f"Unknown verb {verb!r} in tool {tool_name!r}"

    except B1Exception as exc:
        return format_odata_error(exc, resource=alias, key=args.get(key_field))


def dispatch_crossjoin(client: B1Client, args: dict[str, Any]) -> str:
    """Execute a crossjoin tool call and return formatted markdown."""
    entities: list[str] = args.get("entities", [])
    if len(entities) < 2:
        return "Error: crossjoin requires at least 2 entity names in 'entities'."

    try:
        qb = client.crossjoin(*entities)
        if args.get("expand"):
            qb = qb.expand(args["expand"])
        if args.get("filter"):
            qb = qb.filter(args["filter"])
        if args.get("apply"):
            qb = qb.apply(args["apply"])
        if args.get("orderby"):
            qb = qb.orderby(args["orderby"])
        if args.get("top"):
            qb = qb.top(args["top"])
        if args.get("skip"):
            qb = qb.skip(args["skip"])
        rows = qb.execute()
        if not rows:
            return f"$crossjoin({', '.join(entities)}) — no rows returned."
        # Format as simple markdown table from dict keys of first row
        all_keys: list[str] = []
        for row in rows:
            for k in row:
                if k not in all_keys:
                    all_keys.append(k)
        header = " | ".join(all_keys)
        sep = " | ".join(["---"] * len(all_keys))
        lines = [f"### crossjoin({', '.join(entities)})", "", f"| {header} |", f"| {sep} |"]
        for row in rows[:50]:
            cells = " | ".join(str(row.get(k, "")) for k in all_keys)
            lines.append(f"| {cells} |")
        if len(rows) > 50:
            lines.append(f"\n_Showing 50 of {len(rows)} rows._")
        return "\n".join(lines)
    except ValueError as exc:
        return f"Error: {exc}"
    except B1Exception as exc:
        return format_odata_error(exc)


def dispatch_query_service(client: B1Client, args: dict[str, Any]) -> str:
    """Execute a query_service tool call and return formatted markdown."""
    query_path: str = args.get("query_path", "")
    if not query_path:
        return "Error: 'query_path' is required."

    try:
        qb = client.query_service(query_path)
        if args.get("expand"):
            qb = qb.expand(args["expand"])
        if args.get("filter"):
            qb = qb.filter(args["filter"])
        if args.get("apply"):
            qb = qb.apply(args["apply"])
        if args.get("orderby"):
            qb = qb.orderby(args["orderby"])
        if args.get("top"):
            qb = qb.top(args["top"])
        if args.get("skip"):
            qb = qb.skip(args["skip"])
        rows = qb.execute()
        if not rows:
            return f"QueryService {query_path!r} — no rows returned."
        all_keys: list[str] = []
        for row in rows:
            for k in row:
                if k not in all_keys:
                    all_keys.append(k)
        header = " | ".join(all_keys)
        sep = " | ".join(["---"] * len(all_keys))
        lines = [f"### query_service({query_path})", "", f"| {header} |", f"| {sep} |"]
        for row in rows[:50]:
            cells = " | ".join(str(row.get(k, "")) for k in all_keys)
            lines.append(f"| {cells} |")
        if len(rows) > 50:
            lines.append(f"\n_Showing 50 of {len(rows)} rows._")
        return "\n".join(lines)
    except ValueError as exc:
        return f"Error: {exc}"
    except B1Exception as exc:
        return format_odata_error(exc)


# ── Demo (no live SAP required) ───────────────────────────────────────────────

def demo_tool_registry() -> None:
    """Print the generated toolset without connecting to SAP."""
    section("1. Building tool registry from Elite resource catalog")
    registry = build_tool_registry()
    print(f"\n  Registered {len(registry)} tools across {len(_ALIAS_TO_MODEL)} aliases:\n")
    for name, tool in registry.items():
        schema = tool["inputSchema"]
        n_props = len(schema.get("properties", {}))
        n_req = len(schema.get("required", []))
        print(f"  {name:<40s}  props={n_props:2d}  required={n_req}")

    section("2. Inspect a single tool definition")
    tool = registry["orders_patch"]
    print(f"\n  name:        {tool['name']}")
    print(f"  description: {tool['description'][:90]}...")
    props = list(tool["inputSchema"]["properties"].keys())
    print(f"  properties:  {props[:8]}{'...' if len(props) > 8 else ''}")
    print(f"  required:    {tool['inputSchema']['required']}")

    section("3. Enumerate all Elite resources")
    print()
    for desc in list_elite_resources():
        print(
            f"  {desc.alias:<40s}  "
            f"{desc.endpoint:<35s}  "
            f"key={desc.key_field:<12s}  "
            f"category={desc.category}"
        )

    section("4. OData grammar system prompt (first 400 chars)")
    prompt = odata_query_system_prompt()
    print(f"\n{prompt[:400]}...")

    section("5. Error formatting examples (no SAP required)")
    from b1sl.b1sl.exceptions.exceptions import (
        B1AuthError,
        B1NotFoundError,
        B1ValidationError,
        SAPConcurrencyError,
    )
    errors = [
        (SAPConcurrencyError("mismatch", endpoint="Orders"), "orders", 42),
        (B1NotFoundError("not found"), "items", "PHANTOM"),
        (B1AuthError("session expired"), None, None),
        (
            B1ValidationError(
                "bad request",
                details={"error": {"message": {"lang": "en-US", "value": "CardCode is required"}}},
            ),
            "business_partners",
            None,
        ),
    ]
    for exc, resource, key in errors:
        msg = format_odata_error(exc, resource=resource, key=key)
        print(f"\n  [{type(exc).__name__}]\n  {msg[:160]}")


# ── Live demo (requires SAP connection) ──────────────────────────────────────

def demo_live(client: B1Client) -> None:
    """Run a live query against items and format the result."""
    section("6. Live: list first 3 items with $select")
    resource = client.items
    page = (
        resource.select("ItemCode,ItemName,QuantityOnStock")
        .top(3)
        .execute()
    )
    text = format_collection(page, title="Items (first 3)", has_more=page.has_more)
    print(f"\n{text}")

    if page:
        section("7. Live: get single item by key")
        key = page[0].item_code or page[0].model_dump(by_alias=True).get("ItemCode")
        if key:
            item = resource.get(key)
            text = format_entity(item, title=f"Item {key}")
            print(f"\n{text[:600]}{'...' if len(text) > 600 else ''}")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Always run the no-network demo
    demo_tool_registry()

    # Attempt live demo if SAP credentials are available
    try:
        env = B1Environment.load()
        print("\n\nSAP credentials found — running live demo...")
        with B1Client(env.config) as client:
            demo_live(client)
    except Exception as e:
        print(f"\n\n[Live demo skipped — no SAP connection: {e}]")
