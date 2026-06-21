# 17 — Semantic Layer (`sml.svc`)

**HANA-only feature.** SAP B1 on HANA exposes analytical calculation views as
read-only OData v4 collections through a separate service root:

```
GET https://<host>:50000/b1s/v2/sml.svc/<QueryName>?$select=...&$filter=...
```

Common built-in queries include `InventoryStatusQuery` (stock / committed /
ordered / available by warehouse), but the available set depends on your SAP
B1 version and any customer-specific HANA views.

## Accessing a Semantic Layer query

Use `get_resource()` — the canonical way to bind any endpoint that isn't an
Elite alias:

```python
from b1sl.b1sl.client import B1Client
from b1sl.b1sl.models.base import B1Model
from b1sl.b1sl.models.paginated_result import PaginatedResult

with B1Client(config) as client:
    inventory = client.get_resource(B1Model, "sml.svc/InventoryStatusQuery")

    result = (
        inventory
        .select(
            "ItemCode", "ItemDescription",
            "InStockQuantity", "CommittedQuantity",
            "OrderedQuantity", "AvailableQuantity",
            "WarehouseCode", "WarehouseName",
        )
        .filter(
            "(WarehouseCode eq '100' or WarehouseCode eq '1000')"
            " and ItemGroup eq 'REFACCIONES'"
            " and contains(ItemDescription,'MIWE')"
        )
        .orderby("ItemCode")
        .top(20)
        .execute()
    )
    assert isinstance(result, PaginatedResult)

    for row in result:
        extras = row.model_extra or {}
        print(extras["ItemCode"], extras["AvailableQuantity"])
```

The adapter appends the endpoint string directly to the base URL, so
`"sml.svc/InventoryStatusQuery"` resolves to
`.../b1s/v2/sml.svc/InventoryStatusQuery` with no extra configuration.

## Full fluent surface

`get_resource()` returns a `GenericResource` with the complete read API:

| Method | OData param |
|---|---|
| `.select(*fields)` | `$select` |
| `.filter(expr)` | `$filter` — supports `contains()`, `eq`, `or`, etc. |
| `.orderby(expr, desc=False)` | `$orderby` |
| `.top(n)` | client-side cap, collected across pages |
| `.skip(n)` | `$skip` offset |
| `.page_size(n)` | SAP server-side page size (`B1S-PageSize` header) |
| `.execute()` | single page → `PaginatedResult` |
| `.list(query)` | single page → `PaginatedResult` |
| `.stream()` | auto-paginate → `Generator[B1Model]` |
| `.count()` | `GET sml.svc/<QueryName>/$count` |

## Pagination

```python
# Manual paging with skip
page1 = inventory.filter("ItemGroup eq 'REFACCIONES'").skip(0).top(20).execute()
page2 = inventory.filter("ItemGroup eq 'REFACCIONES'").skip(20).top(20).execute()

# Manual paging with next_params (follows @odata.nextLink cursors)
assert isinstance(page1, PaginatedResult)
page = page1
while page.has_more:
    page = inventory.list(params=page.next_params)

# Automatic streaming (follows @odata.nextLink across all pages)
for row in inventory.filter("ItemGroup eq 'REFACCIONES'").stream():
    process(row)
```

## Row access

Rows are `B1Model` instances with `extra="allow"`, so every SAP-returned field
is accessible via `model_extra`:

```python
extras = row.model_extra or {}
extras["ItemCode"]          # "0400011000035"
extras["AvailableQuantity"] # 112.0
```

> **SAP quirk:** some sml.svc columns return the string `"-NULL-"` instead of
> JSON `null` (e.g. `InventoryUoMName` for items with no UoM). Values are
> passed through as-is.

## Async client

```python
from b1sl.b1sl.async_client import AsyncB1Client

async with AsyncB1Client(config) as client:
    inventory = client.get_resource(B1Model, "sml.svc/InventoryStatusQuery")
    result = await (
        inventory
        .select("ItemCode", "AvailableQuantity", "WarehouseCode")
        .filter("WarehouseCode eq '100' and ItemGroup eq 'REFACCIONES'")
        .orderby("ItemCode")
        .top(20)
        .execute()
    )
```

## Related

- `docs/08-dynamic-resources.md` — `get_resource()` pattern in depth
- `examples/24_semantic_layer.py` — runnable example with pagination
