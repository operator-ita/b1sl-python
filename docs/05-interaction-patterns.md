# Interaction Patterns & Query Design

## Overview
The SDK supports three distinct "Styles" of interaction. Choosing the right one is key to building maintainable, performant SAP B1 integrations. 

| Style | Key Tool | Best For... | Type Safety |
| :--- | :--- | :--- | :--- |
| **Pythonic** | `fields` (F constants) | Enterprise core, complex logic | **High** (Auto-complete) |
| **Hybrid** | F + Strings | UDFs, Custom Tables | **Medium** |
| **SAP-Pure** | Raw Strings | Porting existing API docs | **Low** |

## 1. Pattern: Pythonic (The Senior Way)
Highly recommended for production. It uses `fields` (generated as `F`) to map attributes. This prevents typos and enables IDE and type-checker support.

```python
from b1sl.b1sl import fields as F

# Fluent query (Advanced)
# .stream() handles all pages automatically
async for item in client.items.filter(F.Item.item_code.startswith("A")).stream():
    print(item.item_name)
    
# .execute() returns only the first page
results = await client.items.top(5).execute()
```

> [!TIP]
> **Preferred Mutation Pattern: Surgical Deltas**.
> Although you *can* modify a fetched object and send it back, the recommended pattern is to create a fresh, minimal instance of the model for updates (e.g., `en.Item(item_name="New")`). This generates a "Delta" payload, which is safer, faster, and avoids overwrite conflicts. See [Architecture](./01-architecture.md) for the technical rationale.

## 2. Pattern: Hybrid (UDF Support)
Use this when you need an SAP core entity mixed with User-Defined Fields.

```python
bp = await client.business_partners.get(
    "C0001",
    select=[F.BusinessPartner.card_name, "U_Segmento"], # Mix!
)

# Recommended: Explicit UDF access via the .udfs mapping
custom_val = bp.udfs["U_Segmento"]

# Legacy: Fallback access using .get()
custom_val = bp.get("U_Segmento")
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
active_users = await users_resource.filter(F.User.locked == "tNO").execute()
```

The recommended way to build complex OData requests is using the fluent **Query Builder**:

```python
from b1sl.b1sl import fields as F
from datetime import date

# Fluent queries are type-safe and pythonic!
# Use .execute() for single-page results
results = await client.items.filter(
    (F.Item.quantity_on_stock > 0) & (F.Item.valid_from >= date(2024, 1, 1))
).select(
    F.Item.item_code, 
    F.Item.item_name
).orderby(
    F.Item.item_code
).top(3).execute()

# Use .stream() for full collections
async for item in client.items.filter(F.Item.quantity_on_stock > 100).stream():
    process(item)
```

For more details on operators and logic composition, see [10-odata-query-builder.md](./10-odata-query-builder.md).

### Import Styles
The SDK supports two equivalent ways to import field constants:
1. **Direct**: `from b1sl.b1sl.fields import Item` (Simple, used in Quick Starts).
2. **Aliased**: `from b1sl.b1sl import fields as F` (Recommended for complex queries to avoid name collisions).

### Pro Tip: surgical expansion
**Always `$select` what you need.** Requesting complete objects with `expand` significantly degrades SAP Service Layer performance. Use the SDK's surgical expand (passing a dict) to only fetch the fields you need from the joined entity.
