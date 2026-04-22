# b1sl-python
### Modern, async-first Python SDK for SAP Business One Service Layer.

![b1sl Banner](docs/assets/hero-banner.png.png)

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2-orange.svg)](https://docs.pydantic.dev/)
[![Built with httpx](https://img.shields.io/badge/HTTP-httpx-blueviolet.svg)](https://www.python-httpx.org/)

b1sl is a high-performance SDK for the SAP B1 Service Layer, designed around concurrency, type safety, and developer experience. It covers the full lifecycle of a SAP integration — from single-record reads to transactional batch operations over large paginated datasets.

---

## Key Features

- **Async-First Architecture**: Built on `httpx` for non-blocking I/O. Full sync client parity for scripts and non-async contexts.
- **Type Safety**: Pydantic v2 integration for all SAP entities, with IDE autocomplete and runtime validation.
- **Smart Session Management**: Automatic 401 re-authentication with internal locking to prevent license exhaustion.
- **Session Hydration**: Reuse existing `B1SESSION` IDs across serverless functions or Temporal activities.
- **Optimistic Concurrency**: Automated ETag handling with smart cache invalidation on 412 conflicts.
- **Pythonic Querying**: Fluent OData builder with operator overloading (`F.ItemCode == "A001"`) and type-safe field access.
- **Transparent Pagination**: Automatic `nextLink` handling via Python generators — `async for item in client.items.stream()`.
- **`$batch` Support**: Group multiple operations into a single HTTP round-trip with full changeset atomicity.
- **Dynamic UDFs**: Schema-aware proxy for type-safe interaction with User Defined Fields, including opt-in Pydantic validation.
- **Observability**: Structured logging and event hooks for performance monitoring.
- **Safe Development**: Global and per-request Dry Run mode to intercept write operations without hitting SAP.

---

## Installation

```bash
# Using pip
pip install b1sl-python

# Using uv
uv add b1sl-python
```

---

## Quick Start

```python
import asyncio
from b1sl.b1sl import AsyncB1Client, B1Config

async def main():
    config = B1Config.from_env()

    async with AsyncB1Client(config) as b1:
        item = await b1.items.get("I1000")
        print(f"Item: {item.item_name}")

        # UDF access via protected mapping proxy
        print(f"Custom color: {item.udfs['U_Color']}")

asyncio.run(main())
```

---

## Pythonic Querying

Experience a fluent OData builder that uses operator overloading. You can choose between the zero-import **`F` Proxy** (requires SAP CamelCase names) or **Static Constants** (provides Pythonic snake_case autocomplete).

```python
from b1sl.b1sl.resources.odata import F
from b1sl.b1sl.fields import Item

# 1. Dynamic F Proxy (Quick, use SAP field names)
items = await b1.items.filter(F.QuantityOnStock > 0).top(5).execute()

# 2. Static fields (Type-safe, uses Pythonic snake_case autocomplete)
items = await b1.items.filter(Item.quantity_on_stock > 0).top(5).execute()

for item in items:
    print(f"[{item.item_code}] {item.item_name}")
```

---

## Transparent Pagination

`.execute()` returns only the first page SAP gives you. `.stream()` transparently follows every `odata.nextLink` until the dataset is exhausted.

```python
# Silently incomplete for large collections:
first_page = await b1.items.execute()         # → 20 items (SAP's default page)

# Full dataset, zero boilerplate:
async for item in b1.items.stream():          # → all items, all pages
    process(item)

# .top(N) is a hard global cap — not a page size:
async for item in b1.items.top(100).stream(page_size=20):
    ...  # exactly 100 items, fetched in batches of 20

# Safety ceiling on HTTP requests for large tables:
async for item in b1.items.stream(page_size=50, max_pages=5):
    ...  # at most 250 items, at most 5 requests

# Filters are preserved across every page boundary:
async for item in b1.items.filter(F.ItemType == "itItems").stream():
    assert item.item_type == "itItems"  # guaranteed on page 2, 3, ...
```

The sync client has full parity:

```python
from itertools import islice
from b1sl.b1sl import B1Client

with B1Client(config) as b1:
    for item in b1.items.top(50).stream(page_size=10):
        print(item.item_code)

    # islice limits consumption — not HTTP requests.
    # Use .top(N) when you want to limit requests.
    first_5 = list(islice(b1.items.stream(page_size=20), 5))
```

---

## `$batch` Requests

Group multiple operations into a single HTTP round-trip. Use changesets for atomic write transactions.

```python
from b1sl.b1sl import entities as en

async with AsyncB1Client(config) as b1:
    async with b1.batch() as batch:
        # Reads — enqueued, not executed
        await batch.items.top(1).execute()
        await batch.business_partners.top(1).execute()

        # Atomic changeset — all succeed or all fail
        async with batch.changeset() as cs:
            await cs.items.create(en.Item(item_code="B001", item_name="New Item"))
            await cs.items.update("A001", en.Item(item_name="Renamed"))

        results = await batch.execute()

    if results.all_ok:
        print(f"Created/Updated items successfully")
    else:
        for r in results.failed:
            print(f"Operation {r.index} failed: {r.error}")
```

---

## Dynamic UDF Handling

Schema discovery, type-safe access, and opt-in Pydantic validation — no manual model extensions required.

```python
# Constructor injection
new_item = en.Item(item_code="NEW", udfs={"U_Category": "Hardware"})

# Surgical update
await b1.items.update("A001", en.Item(udfs={"U_Status": "Active"}))

# Schema discovery
schema = await b1.items.get_udf_schema()
print(schema)                        # UDFSchema(table='OITM', fields=12)
print("U_Category" in schema)        # True
print(schema["U_Category"].type)     # 'db_Alpha'

# Opt-in validation — generates a scoped Pydantic model on demand
DynamicUDFs = schema.to_pydantic_model("ItemUDFs")
validated = DynamicUDFs.model_validate({"U_Category": "Hardware"})

# Or the full shortcut: validate + serialize in one call
payload = schema.validate_and_dump({"U_Category": "Hardware"})
await b1.items.update("A001", en.Item(udfs=payload))
```

> [!IMPORTANT]
> The `.udfs` proxy enforces the `U_` prefix to prevent accidental overwrites of SAP core fields.

---

## Advanced Usage: FastAPI Integration

b1sl is optimized for modern web frameworks. Use the Lifespan pattern to share a single connection pool across all requests.

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

@app.get("/items")
async def list_items():
    # Stream the full catalog without loading it all into memory
    return [item async for item in b1_client.items.stream(page_size=100)]
```

---

## Architecture Overview

| Feature | Implementation | Benefit |
|:---|:---|:---|
| **HTTP Engine** | `httpx` (Async + Sync) | Superior performance, timeouts, connection pooling |
| **Data Models** | Pydantic v2 | Runtime validation, IDE autocomplete, zero surprises |
| **Auth** | Auto-retry 401 + Session Hydration | Zero-downtime in serverless and long-running contexts |
| **Concurrency** | Shared connection pool + internal locking | Prevents SAP license exhaustion under concurrent load |
| **Pagination** | Generator-based `nextLink` follower | Memory-efficient iteration over arbitrarily large datasets |
| **Batch** | `RecordingAdapter` proxy pattern | Full SDK API reuse inside transactions, no new methods to learn |
| **UDFs** | `UDFSchema` container + dynamic Pydantic | Schema discovery, validation, and serialization in one object |

---

## Why b1sl?

SAP Business One Service Layer is sensitive to session limits and licensing costs. Traditional wrappers often create redundant connections, leading to overhead and frequent auth failures. Beyond auth, naive implementations silently truncate paginated results and require manual OData string construction.

b1sl addresses the full stack of these concerns:

1. **Session Persistence**: Long-lived sessions with atomic re-authentication and internal locking.
2. **Complete Data Access**: `.stream()` ensures you never silently miss records due to SAP's default page size.
3. **Transactional Integrity**: `$batch` with changesets gives you atomicity without writing multipart HTTP by hand.
4. **Zero Learning Curve for New APIs**: The batch proxy reuses the same SDK API — `batch.items.create()` works identically to `b1.items.create()`.

---

## SAP Compatibility

Defaults to **OData V4 (Service Layer v2)**.

| Requirement | Minimum Version |
|:---|:---|
| Verified baseline | Service Layer 1.27 (SAP 10.0 FP 2405) |
| ETag support | Service Layer 1.21+ (March 2021) |
| OData V2 fallback | Configurable via client options |

For the full compatibility timeline, see [docs/02-compatibility.md](https://github.com/operator-ita/b1sl-python/blob/main/docs/02-compatibility.md).

---

## Contributing

Contributions are welcome. Please open an issue to discuss proposed changes before submitting a pull request.

---

## License

MIT © 2026.
