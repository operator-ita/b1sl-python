# Interaction Patterns & Query Design

## Overview
The SDK supports three distinct "Styles" of interaction. Choosing the right one is key to building maintainable, performant SAP B1 integrations. 

| Style | Key Tool | Best For... | Type Safety |
| :--- | :--- | :--- | :--- |
| **Pythonic** | `fields` constants | Enterprise core, complex logic | **High** (Auto-complete) |
| **Hybrid** | `fields` + UDF strings / `F` | UDFs, Custom Tables | **Medium** |
| **SAP-Pure** | Raw Strings | Porting existing API docs | **Low** |

## 1. Pattern: Pythonic (The Senior Way)
Highly recommended for production. It uses the generated `fields` constants to map snake_case attributes to exact SAP names. This prevents typos and enables IDE and type-checker support.

```python
from b1sl.b1sl import fields

# Fluent query (Advanced)
# .stream() handles all pages automatically
async for item in client.items.filter(fields.Item.item_code.startswith("A")).stream():
    print(item.item_name)

# .execute() returns only the first page
results = await client.items.top(5).execute()
```

> [!WARNING]
> Do **not** alias the module as `F` (`from b1sl.b1sl import fields as F`). The
> SDK also exports a different `F` — the raw proxy in `resources.odata` — and
> mixing them up produces broken queries: `proxy_F.Item.item_code` raises
> `AttributeError`, while `fields.Item.item_code` is the real constant.

> [!TIP]
> **Preferred Mutation Pattern: Surgical Deltas**.
> Although you *can* modify a fetched object and send it back, the recommended pattern is to create a fresh, minimal instance of the model for updates (e.g., `en.Item(item_name="New")`). This generates a "Delta" payload, which is safer, faster, and avoids overwrite conflicts. See [Architecture](./01-architecture.md) for the technical rationale.

## 2. Pattern: Hybrid (UDF Support)
Use this when you need an SAP core entity mixed with User-Defined Fields.

```python
from b1sl.b1sl import fields

bp = await client.business_partners.get(
    "C0001",
    select=[fields.BusinessPartner.card_name, "U_Segmento"], # Mix!
)

# UDF access via the protected .udfs mapping
custom_val = bp.udfs["U_Segmento"]
```

In `filter()` expressions, UDFs use the `F` proxy (UDFs have no generated
constant because they are not part of `$metadata`):

```python
from b1sl.b1sl.resources.odata import F

vip = await client.business_partners.filter(F.U_Segmento == "VIP").execute()
```

## 3. Pattern: SAP-Pure (Documentation Style)
Best for testing or copy-pasting code snippets from official SAP documentation or Postman collections.

```python
bp = await client.business_partners.get(
    "C0001",
    select=["CardName", "CardType"],
    expand=["ContactEmployees($select=Name)"]
)
```

## 4. Pattern: Generic Resource Binding (Non-Elite Endpoints)
The SDK intentionally exposes only ~20 critical, ETag-protected endpoints as physical properties on the client (e.g., `client.items`). To interact with the other ~1000 standard Service Layer endpoints, you import the target model and dynamically bind it using `get_resource`.

```python
from b1sl.b1sl import entities as en

# Step 1: Bind the model to its Service Layer Endpoint string
users_resource = client.get_resource(en.User, "Users")

# Step 2: Use it just like an elite property
active_users = await users_resource.filter(fields.User.locked == "tNO").execute()
```

The recommended way to build complex OData requests is using the fluent **Query Builder**:

```python
from datetime import date

from b1sl.b1sl.fields import Item

# Fluent queries are type-safe and pythonic!
# Use .execute() for single-page results
results = await client.items.filter(
    (Item.quantity_on_stock > 0) & (Item.valid_from >= date(2024, 1, 1))
).select(
    Item.item_code,
    Item.item_name
).orderby(
    Item.item_code
).top(3).execute()

# Use .stream() for full collections
async for item in client.items.filter(Item.quantity_on_stock > 100).stream():
    process(item)
```

For more details on operators and logic composition, see [10-odata-query-builder.md](./10-odata-query-builder.md).

### Import Styles
The SDK supports two equivalent ways to import field constants:
1. **Direct**: `from b1sl.b1sl.fields import Item, Order` (preferred — short and explicit).
2. **Module**: `from b1sl.b1sl import fields` then `fields.Item.item_code` (useful when touching many entities).

Never alias the module as `F` — that name belongs to the raw proxy in
`b1sl.b1sl.resources.odata`, and shadowing it is how broken queries like
`F.Item.item_code` (an `AttributeError` on the proxy) end up in code.

### Pro Tip: surgical expansion
**Always `$select` what you need.** Requesting complete objects with `expand` significantly degrades SAP Service Layer performance. Use the SDK's surgical expand (passing a dict) to only fetch the fields you need from the joined entity.
