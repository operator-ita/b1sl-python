"""
Example 24 — SAP B1 Semantic Layer (sml.svc) queries.

HANA-only feature. The Semantic Layer exposes pre-defined HANA analytical
calculation views as read-only OData v4 collections at:

    .../b1s/v2/sml.svc/<QueryName>

Access them via ``get_resource(B1Model, "sml.svc/<QueryName>")``, the same
canonical pattern used for any non-Elite endpoint. The adapter appends the
endpoint string directly to the base URL, so no extra configuration is needed.

Note: some sml.svc columns return the string "-NULL-" instead of JSON null
(e.g. InventoryUoMName for items with no UoM defined) — a SAP server quirk.
"""

from __future__ import annotations

import os

from b1sl.b1sl.config import B1Config, B1Env
from b1sl.b1sl.models.base import B1Model
from b1sl.b1sl.models.paginated_result import PaginatedResult

config = B1Config(
    base_url=os.environ.get("B1SL_BASE_URL", "https://host:50000/b1s/v2"),
    username=os.environ.get("B1SL_USERNAME", "manager"),
    password=os.environ.get("B1SL_PASSWORD", ""),
    company_db=os.environ.get("B1SL_COMPANY_DB", "SBODEMOUS"),
    environment=B1Env.DEV,
)

# ---------------------------------------------------------------------------
# 1. Sync: single page with fluent OData query
# ---------------------------------------------------------------------------

def sync_example() -> None:
    from b1sl.b1sl.client import B1Client

    with B1Client(config) as client:
        inventory = client.get_resource(B1Model, "sml.svc/InventoryStatusQuery")

        result = (
            inventory
            .select(
                "ItemCode", "ItemDescription", "InventoryUoMName",
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

        print(f"Found {len(result)} rows (has_more={result.has_more})")
        for row in result:
            extras = row.model_extra or {}
            print(
                f"  {str(extras.get('ItemCode', '')):30s}"
                f"  wh={extras.get('WarehouseCode')}"
                f"  avail={extras.get('AvailableQuantity')}"
            )


# ---------------------------------------------------------------------------
# 2. Sync: manual pagination with skip
# ---------------------------------------------------------------------------

def sync_paging_example() -> None:
    from b1sl.b1sl.client import B1Client
    from b1sl.b1sl.resources.base import ODataQuery

    with B1Client(config) as client:
        inventory = client.get_resource(B1Model, "sml.svc/InventoryStatusQuery")

        # Option A: explicit skip/top per page via fluent chain
        page1 = (inventory
                 .filter("ItemGroup eq 'REFACCIONES'")
                 .orderby("ItemCode")
                 .skip(0).top(20).execute())
        page2 = (inventory
                 .filter("ItemGroup eq 'REFACCIONES'")
                 .orderby("ItemCode")
                 .skip(20).top(20).execute())
        assert isinstance(page1, PaginatedResult)
        assert isinstance(page2, PaginatedResult)
        print(f"Page 1: {len(page1)} rows, Page 2: {len(page2)} rows")

        # Option B: follow next_params (nextLink cursor — no manual skip math)
        q = ODataQuery(filter="ItemGroup eq 'REFACCIONES'", orderby="ItemCode")
        page = inventory.list(q)
        while page.has_more:
            page = inventory.list(params=page.next_params)
        print("Finished paging")


# ---------------------------------------------------------------------------
# 3. Sync: stream all rows automatically
# ---------------------------------------------------------------------------

def sync_stream_example() -> None:
    from b1sl.b1sl.client import B1Client

    with B1Client(config) as client:
        inventory = client.get_resource(B1Model, "sml.svc/InventoryStatusQuery")
        total = 0
        for _row in inventory.filter("ItemGroup eq 'REFACCIONES'").stream():
            total += 1
        print(f"Streamed {total} total rows")


# ---------------------------------------------------------------------------
# 4. Async: single page
# ---------------------------------------------------------------------------

async def async_example() -> None:
    from b1sl.b1sl.async_client import AsyncB1Client

    async with AsyncB1Client(config) as client:
        inventory = client.get_resource(B1Model, "sml.svc/InventoryStatusQuery")

        result = await (
            inventory
            .select("ItemCode", "AvailableQuantity", "WarehouseCode")
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

        print(f"[async] Found {len(result)} rows")
        for row in result:
            extras = row.model_extra or {}
            print(
                f"  {str(extras.get('ItemCode', '')):30s}"
                f"  avail={extras.get('AvailableQuantity')}"
            )


if __name__ == "__main__":
    sync_example()
    # sync_paging_example()
    # sync_stream_example()
    # import asyncio; asyncio.run(async_example())
