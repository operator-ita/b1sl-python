---
name: b1sl-sdk
description: >
  Modern, async-first Python SDK for SAP Business One Service Layer (b1sl-python).
  Use this skill to interact with SAP B1 entities (Items, Business Partners, Orders,
  Invoices, and 100+ more) using type-safe Pydantic v2 models, a fluent OData query
  builder with operator overloading, automatic session management, and structured
  observability. Covers installation, configuration, async client patterns, query
  building, UDF handling, and the metadata generation pipeline.
---

# SAP B1 Python SDK (b1sl)

## Overview

`b1sl-python` is a **metadata-driven**, async-first SDK for SAP Business One Service Layer.
It automates the entire model and resource layer by parsing SAP's OData metadata, delivering
full type safety, IDE autocompletion, and production-grade session management.

- **PyPI**: `b1sl-python`
- **Repository**: [operator-ita/b1sl-python](https://github.com/operator-ita/b1sl-python)
- **Verified Baseline**: Service Layer **1.27** (SAP 10.0 FP 2405)
- **Protocol**: OData V4 (`v2` endpoint)
- **Minimum for ETags**: Service Layer **1.21+**
- **Companion**: `b1sl.api_gateway` — SAP **API Gateway** client (Crystal Reports layouts → PDF, port 60000, `/rs/v1/`); separate service, separate session, opt-in import. See `docs/20-api-gateway.md`.

---

## Installation

```bash
# Recommended (uv)
uv add b1sl-python

# pip
pip install b1sl-python

# Optional extras
uv add "b1sl-python[django]"   # Django integration
uv add "b1sl-python[generator]" # Metadata generation pipeline
```

---

## Configuration

The SDK uses a hierarchical, environment-agnostic configuration system.

### Required Environment Variables

```bash
B1SL_BASE_URL=https://your-server:50000
B1SL_USERNAME=manager
B1SL_PASSWORD=your_password
B1SL_COMPANY_DB=SBODEMOUS
B1SL_ENV=dev   # dev | test | prod
B1SL_DRY_RUN=0 # 1 to enable Dry Run mode
```

### Loading Config

```python
from b1sl.b1sl import B1Environment, B1Config

# Automatic: reads B1SL_ENV and merges .env + configs/{env}.json
env = B1Environment.load()
config = env.config

# Or directly from environment variables
config = B1Config.from_env()
```

### Environments

| `B1SL_ENV` | Log Format | Use Case |
| :--- | :--- | :--- |
| `dev` (default) | Human-readable | Local development |
| `test` | Human-readable | CI / test isolation |
| `prod` | Structured JSON | Production observability pipelines |
| **Dry Run** | intercepted | `B1SL_DRY_RUN=1`. Intercepts POST/PATCH/DELETE. |

> **Never** store `B1SL_PASSWORD` in `configs/*.json`. Only non-sensitive test data IDs belong there.

### Temporary Dry Run (Context Manager)

You can toggle Dry Run mode temporarily for a specific block of code using the `dry_run()` context manager available in both sync and async clients:

```python
# Globally False, but locally True (Task-Safe via ContextVar)
with b1.dry_run():
    await b1.items.create(new_item) # Intercepted

# Globally True, but locally False (Force execution)
with b1.dry_run(enabled=False):
    await b1.items.update(item) # Sent to SAP

# NOTE: Always use 'with' (sync CM), NOT 'async with', even in async code.
```

---

## ❗ Critical Guidelines: Flat Namespace & Enums
Always use the flat public namespace for models and enums to ensure clean code and IDE support. Never import from `_generated` internal paths.

```python
# ✅ Best Practice: Flat namespace for data models
from b1sl.b1sl import entities as en

# ✅ Best Practice: Field referencing
from b1sl.b1sl.fields import Item, Order   # Static "Pythonic" fields (recommended)
from b1sl.b1sl.resources.odata import F    # Raw proxy — UDFs / dynamic names only

# Use 'en' for model instantiation
new_item = en.Item(item_code="A100", item_name="New Item")
```

---


The recommended client for all production use cases.

### Basic Usage

```python
import asyncio
from b1sl.b1sl import AsyncB1Client, B1Config

async def main():
    config = B1Config.from_env()

    async with AsyncB1Client(config) as b1:
        item = await b1.items.get("A0001")
        print(f"[{item.item_code}] {item.item_name}")

asyncio.run(main())
```

> The `async with` block handles `POST /Logout` automatically — even on exceptions.

### Manual Lifecycle (Long-running services)

```python
client = AsyncB1Client(config)
await client.connect()   # Manual Login
# ... use client ...
await client.aclose()    # Manual Logout
```

### Top 16 Canonical Aliases

| Category | Aliases |
| :--- | :--- |
| **Master Data** | `items`, `business_partners`, `users` |
| **Sales** | `quotations`, `orders`, `delivery_notes`, `invoices`, `incoming_payments` |
| **Purchasing** | `purchase_orders`, `purchase_delivery_notes`, `purchase_invoices`, `vendor_payments` |
| **Operations** | `production_orders`, `journal_entries`, `service_calls`, `activities` |

### Dynamic Access (Any Endpoint)

```python
from b1sl.b1sl.models._generated.entities.inventory import ItemWarehouseInfo

whse_resource = b1.get_resource(ItemWarehouseInfo, "ItemWarehouseInfo")
data = await whse_resource.get("A0001")
```

### Custom Client Alias (Enterprise Pattern)

```python
from b1sl.b1sl import AsyncB1Client
from b1sl.b1sl.resources.async_base import AsyncGenericResource
from b1sl.b1sl.models._generated.entities.inventory import ItemWarehouseInfo

class MyB1Client(AsyncB1Client):
    @property
    def warehouses(self) -> AsyncGenericResource[ItemWarehouseInfo]:
        return self.get_resource(ItemWarehouseInfo, "ItemWarehouseInfo")
```

### High Concurrency with `asyncio.gather`

```python
async with AsyncB1Client(config) as b1:
    codes = ["A0001", "A0002", "A0003"]
    items = await asyncio.gather(*[b1.items.get(c) for c in codes])
```

The SDK uses a shared `httpx.AsyncClient` and an `asyncio.Lock` to prevent session floods.

### Key Async Features

- **401 Auto-Retry**: Expired sessions are transparently renewed and the original request is retried once.
- **Session Hydration**: Reuse an existing `B1SESSION` token across serverless functions or Temporal activities.
- **Optimistic Concurrency (ETags)**: Automated ETag handling with smart cache invalidation on `412` conflicts.

---

## CRUD Operations (Master Data & Transactions)

The SDK provides a consistent set of methods for interacting with resources.

### Create (POST)
Instantiate a model and pass it to the `.create()` method.

```python
from b1sl.b1sl import entities as en

new_item = en.Item(item_code="A0001", item_name="New Item")
await b1.items.create(new_item)
```

### Read (GET)
Fetch by ID or check for existence.

```python
# Fast existence check
if await b1.items.exists("A0001"):
    pass

# Count total records
total = await b1.items.count()
```

### Optimistic Concurrency (ETags)
The SDK manages ETags behind the scenes. Every model instance has a `.etag` property.

```python
item = await b1.items.get("P001")
print(item.etag) # Displays the server-side version token
```

### Update (PATCH) - The "Surgical Delta" Pattern
**Best Practice**: Never resubmit a full object. Only send the fields you want to change.

```python
# Create a minimal object for the update
delta = en.Item(item_name="Updated Name")

# This sends ONLY the name change to SAP
await b1.items.update("A0001", delta)
```

### Delete (DELETE)
```python
await b1.items.delete("A0001")
```

---

## Official Print Layouts to PDF (API Gateway)

Not Service Layer: SAP's **API Gateway** renders Crystal Reports layouts to PDF —
the same document the SAP client prints. Sync and async twins, same surface.

```python
from b1sl.api_gateway import APIGatewayConfig, AsyncAPIGatewayClient

cfg = APIGatewayConfig.from_env()   # B1SL_GATEWAY_BASE_URL + B1SL_* credentials
async with AsyncAPIGatewayClient(cfg) as gw:
    reports = await gw.list_reports()                       # catalog RCRI00xx only
    params = await gw.get_report_parameters("QUT20020")     # layout definition
    pdf = await gw.export_document_pdf("QUT20020", doc_entry=12345)  # DocKey@ set explicitly
```

Rules the client enforces (all learned from the live gateway, none in SAP's manual):
- Failure is signalled by **body**, not HTTP status: `(---)` → `APIGatewayParameterError`
  (retried once — also appears under concurrent exports), `{}` from `LoadCR` →
  `APIGatewayLayoutNotFoundError`, non-`%PDF-` → `APIGatewayPDFError`, bad login →
  `200` + `{"code":-1}` → `APIGatewayAuthError`.
- Empty nullable parameters are omitted; `xsd:date` needs explicit ISO values
  (ranges = two strings in one inner array); never trust the preloaded `DocKey@`.
- Document-bound layout codes (`QUT200xx`…) are **not** discoverable by API — read them
  in Print Layout Designer and version the mapping in your app.
- `max_concurrent_exports` (default 3) bounds parallel renders per client.

## Transparent Pagination Streams

When dealing with large datasets, SAP Service Layer automatically paginates results. The SDK provides a `.stream()` method to transparently handle these pages using Python generators.

### Usage
Available on any resource or builder.

```python
from b1sl.b1sl.fields import Item

# 1. Async iteration
async for item in b1.items.filter(Item.quantity_on_stock > 0).stream(page_size=100):
    process(item)

# 2. Sync iteration — same constants, same semantics
for item in b1.items.filter(Item.quantity_on_stock > 5).stream():
    process(item)
```

### Configuration
- **`page_size`**: Controls `B1S-PageSize` header (HTTP efficiency).
- **`max_pages`**: Safety limit on number of HTTP requests.
- **`.top(N)`**: Hard global limit on total items yielded across all pages.

### Common Patterns
- **Progress**: `total = await b1.items.count(); async for i in b1.items.stream(): ...`
- **Collect**: `items = [i async for i in b1.items.stream()]`
- **Safety**: `.stream(max_pages=5)`

### Guarantee
The SDK ensures that all query parameters (`$filter`, `$select`, etc.) are re-applied to every subsequent page fetch, even if SAP omits them in the `nextLink`.

---

## OData $batch Operations (Performance & Atomicity)

The SDK supports grouping multiple operations into a single HTTP request using a Proxy-based recording pattern.

### Use Case
1. **High Concurrency**: Fetching hundreds of records using generic queries in one Go.
2. **Transaction Integrity**: Ensuring multiple creates/updates succeed or fail together as a unit.

### Basic Pattern
```python
async with b1.batch() as batch:
    # Operations are enqueued via Recording Proxy
    await batch.items.top(1).execute()
    
    # Atomic ChangeSet scope
    async with batch.changeset() as cs:
        await cs.items.create(en.Item(item_code="B1001"))
        await cs.orders.create(new_order)
    
    # Dispatch and parse results
    results = await batch.execute()
```

### Result Analysis
Results are flattened and indexed according to their original enqueueing order.
```python
if results.all_ok:
    print(f"Operation 0 found {len(results[0].entity)} items")
    print(f"New Item Code: {results[2].entity.item_code}")
else:
    for r in results.failed:
        print(f"Op {r.index} failed: {r.error}")
```

### Error Handling & Atomicity
- **Partial Success**: Top-level operations are independent. If one fails, others still succeed.
- **Atomic ChangeSets**: If one operation inside a `changeset()` fails, the **entire** ChangeSet is rolled back.
- **No Exceptions**: `batch.execute()` returns results even on failure. Use `results.all_ok` or `results.failed`.
- **Sync parity**: `B1Client.batch()` works identically with plain `with` blocks and a sync `execute()`.
- **Dry Run aware**: under `with b1.dry_run():`, `batch.execute()` returns synthesized per-op `204`s without sending anything to SAP.

> [!IMPORTANT]
> **OData Rule**: `GET` operations are **not permitted** inside a `changeset()` block. The SDK will raise a `ValueError` if this is attempted.


---

## Error Handling

The SDK maps Service Layer HTTP errors to specialized Python exceptions for cleaner flow control:

- **`B1NotFoundError`**: Resource missing (404).
- **`B1ValidationError`**: Bad request or validation failure (400).
- **`SAPConcurrencyError`**: ETag version mismatch (412).
- **`B1AuthError`**: Authentication or session failure (401).
- **`B1Exception`**: Base class for all SDK-specific errors.

### Pattern: Safe Existence Check
Instead of catching 404s manually, use the `.exists()` helper:

```python
if await b1.items.exists("A0001"):
    # item exists, proceed with logic
    pass
```

### Pattern: Defensive Error Parsing
The SDK handles cases where SAP returns string-based error nodes instead of dictionaries, ensuring `e.details` is always safe to inspect if it contains valid JSON.

---

## FastAPI Integration

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
from b1sl.b1sl import AsyncB1Client, B1Config

b1_client: AsyncB1Client | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global b1_client
    b1_client = AsyncB1Client(B1Config.from_env())
    await b1_client.connect()
    yield
    await b1_client.aclose()

app = FastAPI(lifespan=lifespan)

@app.get("/items/{item_code}")
async def get_item(item_code: str):
    return await b1_client.items.get(item_code)
```

---

## SQL Queries

Execute stored SQL definitions via the `SQLQueries` endpoint.  Use `client.sql_queries` (Elite alias) on both sync and async clients.

### Running a stored query

```python
from b1sl.b1sl import B1Client, B1Config

with B1Client(B1Config.from_env()) as client:
    # No parameters — returns first page
    result = client.sql_queries.run("sql04")
    print(f"{len(result)} rows, has_more={result.has_more}")

    # Named parameters (match :name placeholders in SqlText, case-sensitive)
    result = client.sql_queries.run("sql01", docTotal=100.0, docPartner="C001")

    # Stream all pages
    for row in client.sql_queries.run_stream("sql04", page_size=50, max_pages=10):
        process(row)
```

### Typed rows via Pydantic

```python
from pydantic import BaseModel

class ItemRow(BaseModel):
    ItemCode: str
    OnHand: float | None = None

result = client.sql_queries.run("sql04")
typed = result.to_pydantic(ItemRow)
print(typed[0].ItemCode)
```

### Async client

```python
async with AsyncB1Client(config) as b1:
    result = await b1.sql_queries.run("sql04")
    async for row in b1.sql_queries.run_stream("sql04", page_size=50):
        await process(row)
```

### Error handling

| SAP code | Exception | Cause |
| :--- | :--- | :--- |
| `"702"` | `B1SqlNotAllowedError` | Table not in `b1s_sqltable.conf` allowlist |
| `"703"` | `B1SqlNotAllowedError` | Column in `ColumnExcludeList` |
| `"704"` | `B1SqlParamError` | Wrong parameter name, count, or type |

Both `B1SqlNotAllowedError` and `B1SqlParamError` are subclasses of `B1ValidationError`.

```python
from b1sl.b1sl.exceptions.exceptions import B1SqlNotAllowedError, B1SqlParamError

try:
    result = client.sql_queries.run("sql04", wrongParam=1)
except B1SqlNotAllowedError as e:
    print(f"Table/column blocked [{e.sap_code}]: {e}")
except B1SqlParamError as e:
    print(f"Parameter error: {e}")
```

> Reference: `docs/reference/sl/sql-queries.md`

---

## SQL Query Composer (MCP / AI Agent helpers)

`b1sl.contrib.mcp` provides grammar constants and prompt helpers that let an
LLM (Claude, GPT, etc.) generate valid SAP SL SQL without hallucinating
unsupported constructs.

### The problem

LLMs frequently write SQL that SAP SL silently rejects:

| LLM writes | SL response |
|---|---|
| `CASE WHEN … END` | parse error |
| `COALESCE(col, 0)` | parse error |
| `WITH cte AS (…)` | parse error |
| `ROW_NUMBER() OVER (…)` | parse error |
| `FROM (SELECT …) AS sub` | parse error |

### Ground the LLM before asking it to write SQL

```python
from b1sl.contrib.mcp.grammar import sql_grammar_system_prompt

# Prepend to your LLM system prompt
system = sql_grammar_system_prompt()          # includes table list
system_no_tables = sql_grammar_system_prompt(include_tables=False)

messages = [
    {"role": "system", "content": system},
    {"role": "user", "content": "Write SQL to get all items with stock > 0"},
]
# LLM will only use: SELECT, WHERE, ISNULL, LOWER, etc. — no CASE WHEN
```

### Grammar constants for validation

```python
from b1sl.contrib.mcp import (
    SUPPORTED_KEYWORDS,   # frozenset — SELECT, JOIN, GROUP BY, UNION…
    SUPPORTED_FUNCTIONS,  # frozenset — SUM, AVG, ISNULL, LOWER…
    UNSUPPORTED_COMMON,   # frozenset — CASE WHEN, COALESCE, CTE, CAST…
)

# Post-validate generated SQL before sending to SAP
sql_upper = generated_sql.upper()
violations = [kw for kw in UNSUPPORTED_COMMON if kw in sql_upper]
if violations:
    raise ValueError(f"Unsupported constructs: {violations}")
```

### Full MCP agent loop: describe → generate → store → run

```python
from b1sl.contrib.mcp.grammar import sql_grammar_system_prompt
from b1sl.contrib.mcp.schemas import sql_query_tool_definition
from b1sl.contrib.mcp.formatters import format_sql_result

# 1. Ground the LLM
system_prompt = sql_grammar_system_prompt()

# 2. LLM generates SQL → store in SAP
with B1Client(config) as b1:
    b1.sql_queries.create(en.SQLQuery(
        sql_code="agent_items_low_stock",
        sql_name="Agent: Items with low stock",
        sql_text='SELECT "ItemCode", "ItemName", "OnHand" FROM "OITM" WHERE "OnHand" < :threshold',
        param_list="threshold",
    ))

    # 3. Describe and expose as MCP tool
    info = b1.sql_queries.describe("agent_items_low_stock")
    tool = sql_query_tool_definition(info)
    # → {"name": "sql_agent_items_low_stock", "inputSchema": {"required": ["threshold"], …}}

    # 4. Agent calls the tool → run and format for LLM context
    result = b1.sql_queries.run("agent_items_low_stock", threshold=10)
    context = format_sql_result(result, title="Low Stock Items")
```

### Key SQL rules to embed in your prompts

| Rule | Detail |
|---|---|
| Write unquoted identifiers | SL normalises `ItemCode` → `"ItemCode"` (HANA) / `[ItemCode]` (MSSQL) |
| Always alias columns | Aliases become JSON keys — `SELECT ItemCode as Code` → `{"Code": "…"}` |
| Use `:paramName` for params | `WHERE "DocTotal" > :docTotal` — pass at `run(code, docTotal=100)` |
| `ISNULL` = `IFNULL` | Both are cross-backend; SL normalises transparently |
| No subquery aliases | `FROM (SELECT …) AS sub` is NOT supported |

---

## OData Query Builder

Fluent, type-safe interface. No string concatenation needed. Lead with the **Static Field Constants** (`b1sl.b1sl.fields`); reach for the raw **`F` proxy** only for UDFs and dynamic names.

### Field Referencing Styles

| Style | Variable | Import | Case | Autocomplete |
| :--- | :--- | :--- | :--- | :--- |
| **Static (recommended)** | `Item`, `Order`, etc. | `from b1sl.b1sl.fields import Item, Order` | **Pythonic snake_case** | ✅ Full |
| **Dynamic (UDFs / raw)** | `F` | `from b1sl.b1sl.resources.odata import F` | **SAP CamelCase**, verbatim | ❌ None |

The static constants carry the metadata-verified SAP names — including
irregular spellings a naive conversion gets wrong (`service_call_id` →
`ServiceCallID`, `bplid` → `BPLID`). A typo on a constant raises
`AttributeError` immediately; a typo through `F` becomes a live SAP -1000
error at runtime. Entity-set aliases mirror `entities`: `fields.Order`,
`fields.Invoice`, … resolve to `DocumentFields`.

### Basic Examples

```python
from b1sl.b1sl.fields import Item
from b1sl.b1sl.resources.odata import F

# 1. Static constants (recommended — autocomplete, snake_case, typo-safe)
results = await b1.items.filter(Item.quantity_on_stock > 0).execute()

# 2. F proxy — for UDFs, which have no generated constant
results = await b1.items.filter(F.U_Categoria == "MRO").execute()
```

> Never import the module as `F` (`from b1sl.b1sl import fields as F`): that
> shadows the raw proxy and the two are not interchangeable.

### Operator Reference

| Python Operator | OData Equivalent | Example |
| :--- | :--- | :--- |
| `==` | `eq` | `Item.item_code == 'A001'` |
| `!=` | `ne` | `BusinessPartner.card_code != 'C001'` |
| `>` | `gt` | `Item.quantity_on_stock > 0` |
| `>=` | `ge` | `Order.doc_total >= 100.5` |
| `&` | `and` | `(A) & (B)` |
| `\|` | `or` | `(A) \| (B)` |
| `~` | `not` | `~(A)` |

> **IMPORTANT**: Parentheses are mandatory for logical composition: `(A) & (B)`.

### String Functions

```python
# .contains, .startswith, .endswith
await b1.items.filter(Item.item_name.contains("Cheese")).execute()
```

### Expansions (Surgical)

```python
from b1sl.b1sl.fields import ServiceCall, BusinessPartner

# Dictionary expand — fetches only selected fields from the related entity
sc = await client.service_calls.by_id(1).expand({
    ServiceCall.business_partner: [BusinessPartner.card_code, BusinessPartner.card_name]
}).execute()

# Path-based selection using the '/' operator (never attribute chaining)
sc = await client.service_calls.by_id(1).select(
    ServiceCall.subject,
    ServiceCall.business_partner / BusinessPartner.card_code,
).expand([ServiceCall.business_partner]).execute()
```

### Terminal Methods

| Method | Source | Returns | Behavior |
| :--- | :--- | :--- | :--- |
| **`.execute()`** | Builder | `PaginatedResult[T] \| T` | Executes query, returns **one page** (list-like, with `next_params` / `has_more`) or single object. |
| **`.list()`** | Resource | `PaginatedResult[T]` | One page with pagination metadata; pass `params=page.next_params` for the next page. |
| **`.stream()`** | Either | `Generator` | **Transparent**. Fetches every page until exhaustion. |
| **`.first()`** | Builder | `T \| None` | Adds `$top=1`, executed, returns first or `None`. |

---

## Interaction Patterns

| Style | Tooling | Discovery | Case | Best For |
| :--- | :--- | :--- | :--- | :--- |
| **Pythonic** | `fields` | ✅ Full IDE | snake_case | Default for every metadata field. |
| **Dynamic** | `F` Proxy | ❌ None | CamelCase | UDFs, runtime-built names, generic tools. |
| **Hybrid** | `fields` + raw strings | Mixed | Mixed | Custom tables, advanced OData. |

---

## UDF (User-Defined Field) Handling

The core SDK follows a "Vanilla" policy — `U_*` fields are excluded from generated models to maintain version stability. Three patterns cover UDF access:

### Pattern A — Dynamic `.udfs` Mapping (Recommended)
The most professional way to handle UDFs. Provides a protected namespace on every model.

```python
item = b1.items.get("C100")

# Read/Write via the .udfs proxy (Strictly requires 'U_' prefix)
item.udfs["U_Color"] = "Vibrant Red"
current_color = item.udfs["U_Color"]

# Constructor injection
new_bp = en.BusinessPartner(
    card_code="C2000",
    udfs={"U_Priority": "High"}
)
```

> [!IMPORTANT]
> The `.udfs` mapping **strictly enforces** the `U_` prefix. Attempting to access or set a non-UDF field via this proxy will raise a `KeyError`.

### Pattern B — Typed UDFs (for heavy UDF users)
Declare UDFs as first-class fields in the Override system:

```python
# src/b1sl/b1sl/models/_overrides/inventory.py
from pydantic import Field
from .._generated.entities.inventory import Item as _Item

class Item(_Item):
    my_color: str | None = Field(None, alias="U_RealColor")
    #  ^ Now fully typed with IDE autocomplete
```

> [!NOTE]
> Legacy code may read UDFs via `model.get("U_Color")` (possible because
> `B1Model` uses `extra="allow"`). Discouraged: it does not enforce the `U_`
> prefix, so a typo silently reads a core SAP field. Use `.udfs` instead —
> it supports the full Mapping API, including `.get(key, default)`.

### Pattern C — Dynamic Schema & Validation (Advanced)
Discovery and validation using the metadata-driven `UDFSchema` container.

```python
# 1. Fetch the schema for the resource
schema = await b1.business_partners.get_udf_schema()

# 2. Introspection
if "U_Age" in schema:
    print(f"U_Age info: {schema['U_Age'].description}")

# 3. Validation Loop (the safest way to PATCH)
try:
    # Validates data against SAP metadata (types, sizes) and returns a clean payload
    payload = schema.validate_and_dump({"U_Age": 25, "U_Color": "Red"})
    
    # Surgical Patch using the validated payload
    await b1.business_partners.update(card_code, {"udfs": payload})
except Exception as e:
    print(f"Validation failed: {e}")
```

> [!TIP]
> Use `validate_and_dump` when building UIs or integrations where incoming raw data needs to be verified against the current SAP environment's schema before submission.


---

## Architecture Layers

```
src/b1sl/b1sl/
├── models/
│   ├── _generated/     # AUTO-GENERATED — NEVER edit manually
│   ├── _overrides/     # Handcrafted extensions (calculated props, UDFs)
│   └── entities/       # Public facade — blend of generated + overrides
├── resources/
│   ├── _generated/     # Auto-generated service classes (CRUD + actions)
│   └── async_base.py   # AsyncGenericResource base
└── fields/             # Typed OData field constants (fields.Item.item_code, ...)
```

**Key rules:**
- **`_generated/` is read-only.** All structural changes go through the generator.
- Imports for consumers should always come from `b1sl.b1sl.entities` or `b1sl.b1sl.fields`.
- `B1Model` provides universal: boolean coercion (`tYES`/`tNO`→`bool`), date parsing (`/Date(ms)/`→ISO), and null filtering on `.to_api_payload()`.

---

## Metadata Generation Pipeline

Used when updating models for a new SAP version or adding new entities.

```bash
# Capture metadata from Service Layer and run the pipeline
./scripts/generate_models.sh <version>  # e.g., 1.27
```

**Source files** (place in `metadata/<version>/`):

| File | Source |
| :--- | :--- |
| `metadata_document.xml` | `GET /b1s/v2/$metadata` |
| `service_document.json` | `GET /b1s/v2/` |
| `service_layer_api_reference.html` | SAP API Reference page |

> Use `.real.xml` / `.real.json` suffixes for local production metadata — they are git-ignored and take precedence over generic files.

---

## Django Integration

```python
# Reads B1SL_* variables from Django settings.py
from b1sl.b1sl import B1Config, B1Client

config = B1Config.from_django_settings()
client = B1Client(config)

# Legacy singleton adapter
from b1sl.b1sl.adapter import get_rest_adapter
adapter = get_rest_adapter()  # Thread-safe singleton
```

---

## Resources

| Resource | Link |
| :--- | :--- |
| Full Documentation | [docs/](https://github.com/operator-ita/b1sl-python/tree/main/docs) |
| Architecture | [01-architecture.md](https://github.com/operator-ita/b1sl-python/blob/main/docs/01-architecture.md) |
| Configuration | [03-configuration.md](https://github.com/operator-ita/b1sl-python/blob/main/docs/03-configuration.md) |
| Async Client | [04-async-client.md](https://github.com/operator-ita/b1sl-python/blob/main/docs/04-async-client.md) |
| Interaction Patterns | [05-interaction-patterns.md](https://github.com/operator-ita/b1sl-python/blob/main/docs/05-interaction-patterns.md) |
| OData Query Builder | [10-odata-query-builder.md](https://github.com/operator-ita/b1sl-python/blob/main/docs/10-odata-query-builder.md) |
| Batching Operations | [13-batching.md](https://github.com/operator-ita/b1sl-python/blob/main/docs/13-batching.md) |
| Pagination Streams | [14-pagination-streams.md](https://github.com/operator-ita/b1sl-python/blob/main/docs/14-pagination-streams.md) |
| UDFs & Overrides | [07-overrides-and-udfs.md](https://github.com/operator-ita/b1sl-python/blob/main/docs/07-overrides-and-udfs.md) |
| Contributing | [09-contributing.md](https://github.com/operator-ita/b1sl-python/blob/main/docs/09-contributing.md) |
| Repository | [operator-ita/b1sl-python](https://github.com/operator-ita/b1sl-python) |
