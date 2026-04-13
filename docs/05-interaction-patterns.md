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

# Simple fetch
sc = await client.service_calls.get(TEST_ID, select=[F.ServiceCall.subject])

# Fluent query (Advanced)
results = await client.items.filter(F.Item.item_code.startswith("A")) \
                            .select(F.Item.item_code, F.Item.item_name) \
                            .top(5) \
                            .execute()
```

## 2. Pattern: Hybrid (UDF Support)
Use this when you need an SAP core entity mixed with User-Defined Fields.

```python
sc = await client.service_calls.get(
    TEST_ID,
    select=[F.ServiceCall.subject, "U_OTFecha"], # Mix!
)
custom_val = sc.get("U_OTFecha")
```

## 3. Pattern: SAP-Pure (Documentation Style)
Best for testing or copy-pasting code snippets from official SAP documentation or Postman collections.

```python
sc = await client.service_calls.get(
    TEST_ID,
    select=["Subject", "CustomerCode"],
    expand=["BusinessPartner($select=CardCode)"]
)
```

The recommended way to build complex OData requests is using the fluent **Query Builder**:

```python
from b1sl.b1sl import fields as F
from datetime import date

# Fluent queries are type-safe and pythonic!
results = await client.items.filter(
    (F.Item.quantity_on_stock > 0) & (F.Item.valid_from >= date(2024, 1, 1))
).select(
    F.Item.item_code, 
    F.Item.item_name
).orderby(
    F.Item.item_code
).top(3).execute()
```

For more details on operators and logic composition, see [10-odata-query-builder.md](./10-odata-query-builder.md).

### Import Styles
The SDK supports two equivalent ways to import field constants:
1. **Direct**: `from b1sl.b1sl.fields import Item` (Simple, used in Quick Starts).
2. **Aliased**: `from b1sl.b1sl import fields as F` (Recommended for complex queries to avoid name collisions).

### Pro Tip: surgical expansion
**Always `$select` what you need.** Requesting complete objects with `expand` significantly degrades SAP Service Layer performance. Use the SDK's surgical expand (passing a dict) to only fetch the fields you need from the joined entity.
