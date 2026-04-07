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

sc = client.service_calls.get(
    TEST_ID,
    select=[F.ServiceCall.subject, F.ServiceCall.customer_code],
    expand={
        F.ServiceCall.business_partner: [F.BusinessPartner.card_code],
        F.ServiceCall.item:             [F.Item.item_code, F.Item.item_name]
    }
)
# Access data directly from typed attributes
bp_code = sc.business_partner.card_code if sc.business_partner else "N/A"
```

## 2. Pattern: Hybrid (UDF Support)
Use this when you need an SAP core entity mixed with User-Defined Fields.

```python
sc = client.service_calls.get(
    TEST_ID,
    select=[F.ServiceCall.subject, "U_OTFecha"], # Mix!
)
custom_val = sc.get("U_OTFecha")
```

## 3. Pattern: SAP-Pure (Documentation Style)
Best for testing or copy-pasting code snippets from official SAP documentation or Postman collections.

```python
sc = client.service_calls.get(
    TEST_ID,
    select=["Subject", "CustomerCode"],
    expand=["BusinessPartner($select=CardCode)"]
)
```

## Advanced Query Design (ODataQuery)
The `ODataQuery` class provides a structured way to handle filtering and sorting:

```python
from b1sl.b1sl.resources.base import ODataQuery

query = ODataQuery(
    filter=f"{F.Item.quantity_on_stock} gt 0",
    top=3,
    select=[F.Item.item_code, F.Item.item_name],
    orderby=f"{F.Item.item_code} asc"
)

results = client.items.list(query)
```

### Pro Tip: surgical expansion
**Always `$select` what you need.** Requesting complete objects with `expand` significantly degrades SAP Service Layer performance. Use the SDK's surgical expand (passing a dict) to only fetch the fields you need from the joined entity.
