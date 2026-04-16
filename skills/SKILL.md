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

---

## Installation

```bash
# Recommended (uv)
uv add b1sl-python

# pip
pip install b1sl-python

# Optional extras
uv add "b1sl-python[hana]"     # SAP HANA driver (hdbcli)
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
# ✅ Best Practice
from b1sl.b1sl import entities as en, fields as F

# Enums are automatically available in 'en'
open_status = en.BoStatus.bost_Open
new_item = en.Item(item_code="A100")
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

## OData Query Builder

Fluent, type-safe interface. No string concatenation needed.

### Import Styles

```python
# Direct (good for simple scripts)
from b1sl.b1sl.fields import Item

# Aliased (recommended for complex queries — avoids name collisions)
from b1sl.b1sl import fields as F
```

### Filtering

```python
from b1sl.b1sl.fields import Item
from datetime import date

results = client.items.filter(
    (Item.quantity_on_stock > 0) & (Item.valid_from >= date(2024, 1, 1))
).select(
    Item.item_code,
    Item.item_name
).orderby(
    Item.item_code
).top(5).execute()
```

### Operator Reference

| Python Operator | OData | Example |
| :--- | :--- | :--- |
| `==` | `eq` | `Item.item_code == 'A001'` |
| `!=` | `ne` | `Item.item_code != 'A001'` |
| `>` | `gt` | `Item.quantity_on_stock > 10` |
| `>=` | `ge` | `Item.price >= 100.5` |
| `<` | `lt` | `Item.on_hand < 10` |
| `<=` | `le` | `Item.on_hand <= 5` |
| `&` | `and` | `(A) & (B)` |
| `\|` | `or` | `(A) \| (B)` |
| `~` | `not` | `~(A)` |

> **Parentheses are mandatory** when composing expressions: `(A) & (B)`, not `A & B`.

### String Functions

```python
client.items.filter(Item.item_name.contains("Cheese")).execute()
client.items.filter(Item.item_code.startswith("A")).execute()
client.items.filter(Item.item_code.endswith("01")).execute()
```

### Expansions (Surgical)

```python
from b1sl.b1sl.fields import ServiceCall, BusinessPartner

# Dictionary expand — fetches only selected fields from the related entity
sc = client.service_calls.by_id(1).expand({
    ServiceCall.business_partner: [BusinessPartner.card_code, BusinessPartner.card_name]
}).execute()

# Path-based selection using '/' operator
sc = client.service_calls.by_id(1).select(
    ServiceCall.subject,
    ServiceCall.business_partner / BusinessPartner.card_code
).expand([ServiceCall.business_partner]).execute()
```

### Terminal Methods

| Method | Behavior |
| :--- | :--- |
| `.execute()` | Returns `list` or single object |
| `.first()` | Adds `$top=1`, returns first result or `None` |

---

## Interaction Patterns

| Style | Tooling | Type Safety | Best For |
| :--- | :--- | :--- | :--- |
| **Pythonic** | `fields` (F constants) | High | Enterprise, complex queries |
| **Hybrid** | F + raw strings | Medium | UDFs, Custom Tables |
| **SAP-Pure** | Raw OData strings | Low | Porting from API docs / Postman |

```python
# Hybrid: mix typed fields with a UDF
sc = client.service_calls.get(
    TEST_ID,
    select=[F.ServiceCall.subject, "U_OTFecha"]
)
custom_val = sc.get("U_OTFecha")
```

---

## UDF (User-Defined Field) Handling

The core SDK follows a "Vanilla" policy — `U_*` fields are excluded from generated models to
maintain version stability. Two patterns cover UDF access:

### Pattern A — Spontaneous Access (no setup required)

`B1Model` uses `extra="allow"`. All UDFs returned by SAP are available via `.get()`:

```python
item = client.items.get("C100")
color = item.get("U_Color", "Not Found")
```

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
└── fields.py           # Typed OData field constants (F.Item.item_code, ...)
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
| UDFs & Overrides | [07-overrides-and-udfs.md](https://github.com/operator-ita/b1sl-python/blob/main/docs/07-overrides-and-udfs.md) |
| Contributing | [09-contributing.md](https://github.com/operator-ita/b1sl-python/blob/main/docs/09-contributing.md) |
| Repository | [operator-ita/b1sl-python](https://github.com/operator-ita/b1sl-python) |
