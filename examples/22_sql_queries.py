"""
Example 22: SQL Queries — Stored SQL Execution via SQLQueries Endpoint

Demonstrates the full lifecycle of the ``client.sql_queries`` Elite alias:
- CRUD on stored SQL definitions (create / get / delete).
- Executing a stored query with ``run()`` — single page.
- Executing with named parameters.
- Streaming all pages with ``run_stream()``.
- Typed rows via ``result.to_pydantic(MyModel)``.
- Error handling for ``B1SqlNotAllowedError`` and ``B1SqlParamError``.
- Async client parity with ``AsyncB1Client``.

SAP reference: ``docs/reference/sl/sql-queries.md``

Prerequisites:
    B1SL_BASE_URL, B1SL_USERNAME, B1SL_PASSWORD, B1SL_COMPANY_DB env vars
    (or a populated .env file at the project root).
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from pydantic import BaseModel

from b1sl.b1sl import AsyncB1Client, B1Client, B1Environment
from b1sl.b1sl import entities as en
from b1sl.b1sl.exceptions.exceptions import B1SqlNotAllowedError, B1SqlParamError

# ── Helpers ───────────────────────────────────────────────────────────────────

DEMO_SQL_CODE = "ex22_items"
DEMO_SQL_WITH_PARAMS_CODE = "ex22_items_by_group"


def section(title: str) -> None:
    print(f"\n{'─' * 70}")
    print(f"  {title}")
    print(f"{'─' * 70}")


# ── Typed row models ──────────────────────────────────────────────────────────

class ItemRow(BaseModel):
    ItemCode: str
    ItemName: str | None = None
    OnHand: float | None = None


class ItemGroupRow(BaseModel):
    ItemCode: str
    ItmsGrpCod: int | None = None


# ── Scenario 1: CRUD on stored SQL definitions ────────────────────────────────

def demo_crud(client: B1Client) -> None:
    """Create, read, and delete a stored SQL definition."""
    section("1. CRUD — Create / Get / Delete a SQL Definition")

    # Idempotent setup: remove leftovers from previous failed runs
    for code in (DEMO_SQL_CODE, DEMO_SQL_WITH_PARAMS_CODE):
        try:
            client.sql_queries.delete(code)
        except Exception:
            pass

    # Create a simple stored query (no parameters)
    query_def = en.SQLQuery(
        sql_code=DEMO_SQL_CODE,
        sql_name="Example 22 — Items",
        sql_text='SELECT T0."ItemCode", T0."ItemName", T0."OnHand" FROM "OITM" T0',
    )
    client.sql_queries.create(query_def)
    print(f"  Created: {DEMO_SQL_CODE}")

    # Create a parameterised query
    param_query = en.SQLQuery(
        sql_code=DEMO_SQL_WITH_PARAMS_CODE,
        sql_name="Example 22 — Items by Group",
        sql_text='SELECT T0."ItemCode", T0."ItmsGrpCod" FROM "OITM" T0 WHERE T0."ItmsGrpCod" = :groupCode',
        param_list="groupCode",
    )
    client.sql_queries.create(param_query)
    print(f"  Created: {DEMO_SQL_WITH_PARAMS_CODE}")

    # Read back
    fetched = client.sql_queries.get(DEMO_SQL_CODE)
    print(f"  Fetched: code={fetched.sql_code!r}, name={fetched.sql_name!r}")


# ── Scenario 2: run() — single page, no params ───────────────────────────────

def demo_run_no_params(client: B1Client) -> None:
    """Execute a stored SQL and inspect the first page."""
    section("2. run() — Single Page, No Parameters")

    result = client.sql_queries.run(DEMO_SQL_CODE)

    print(f"  Rows returned  : {len(result)}")
    print(f"  SQL executed   : {result.sql_text[:60]}...")
    print(f"  Has more pages : {result.has_more}")

    if result:
        row = result[0]
        print(f"  First row      : ItemCode={row.get('ItemCode')!r}, OnHand={row.get('OnHand')}")


# ── Scenario 3: run() — with named parameters ─────────────────────────────────

def demo_run_with_params(client: B1Client) -> None:
    """Execute a parameterised stored query."""
    section("3. run() — Named Parameters")

    # groupCode is an integer parameter in the SQL
    result = client.sql_queries.run(DEMO_SQL_WITH_PARAMS_CODE, groupCode=100)

    print(f"  Items in group 100: {len(result)} rows")
    for row in result:
        print(f"    ItemCode={row.get('ItemCode')!r}")


# ── Scenario 4: run_stream() — paginated stream ───────────────────────────────

def demo_run_stream(client: B1Client) -> None:
    """Stream all rows across pages, with page_size and max_pages controls."""
    section("4. run_stream() — Streaming All Pages")

    # Stream with small page size to force pagination
    total = 0
    for row in client.sql_queries.run_stream(DEMO_SQL_CODE, page_size=5, max_pages=3):
        total += 1

    print(f"  Total rows streamed (up to 3 pages × 5 rows): {total}")
    print("  💡 run_stream() follows @odata.nextLink automatically.")


# ── Scenario 5: result.to_pydantic() — typed rows ────────────────────────────

def demo_to_pydantic(client: B1Client) -> None:
    """Convert raw rows to typed Pydantic model instances."""
    section("5. result.to_pydantic() — Typed Row Access")

    result = client.sql_queries.run(DEMO_SQL_CODE)
    typed_rows = result.to_pydantic(ItemRow)

    print(f"  Validated {len(typed_rows)} rows as ItemRow")
    for row in typed_rows[:3]:
        print(f"    {row.ItemCode!r:<20} OnHand={row.OnHand}")


# ── Scenario 6: Error handling ────────────────────────────────────────────────

def demo_error_handling(client: B1Client) -> None:
    """Demonstrate SQL-specific error handling."""
    section("6. Error Handling — B1SqlNotAllowedError / B1SqlParamError")

    # 6a — Table blocked (SAP code 702)
    blocked_query = en.SQLQuery(
        sql_code="ex22_blocked",
        sql_name="Example 22 — Blocked Table",
        sql_text='SELECT T0."ItemCode" FROM "OSRI" T0',  # OSRI may be blocked
    )
    try:
        client.sql_queries.create(blocked_query)
        result = client.sql_queries.run("ex22_blocked")
        print(f"  ex22_blocked returned {len(result)} rows (table was accessible)")
    except B1SqlNotAllowedError as e:
        print(f"  B1SqlNotAllowedError [{e.sap_code}]: {e}")
        print("  → Fix: add the table to b1s_sqltable.conf on the server")
    except Exception as e:
        print(f"  Other error: {e}")
    finally:
        try:
            client.sql_queries.delete("ex22_blocked")
        except Exception:
            pass

    # 6b — Wrong parameter name (SAP code 704)
    try:
        # DEMO_SQL_WITH_PARAMS_CODE expects :groupCode, passing wrong name
        client.sql_queries.run(DEMO_SQL_WITH_PARAMS_CODE, wrong_param=100)
        print("  No error raised — server accepted unknown param (unexpected)")
    except B1SqlParamError as e:
        print(f"  B1SqlParamError [{e.sap_code}]: {e}")
        print("  → Fix: check ParamList field on the SQLQuery entity")


# ── Scenario 7: Async client ──────────────────────────────────────────────────

async def demo_async(env: B1Environment) -> None:
    """Async client mirrors the sync API with await / async for."""
    section("7. Async Client — AsyncB1Client")

    async with AsyncB1Client(env.config) as b1:
        # One-page run
        result = await b1.sql_queries.run(DEMO_SQL_CODE)
        print(f"  async run()  → {len(result)} rows, has_more={result.has_more}")

        # Streaming pages (max_pages=3 keeps the demo fast on slow servers)
        total = 0
        async for _ in b1.sql_queries.run_stream(DEMO_SQL_CODE, page_size=10, max_pages=3):
            total += 1
        print(f"  async run_stream() → {total} rows (≤ 30, capped at 3 pages)")


# ── Cleanup ───────────────────────────────────────────────────────────────────

def cleanup(client: B1Client) -> None:
    section("Cleanup — Delete Demo SQL Definitions")
    for code in (DEMO_SQL_CODE, DEMO_SQL_WITH_PARAMS_CODE):
        try:
            client.sql_queries.delete(code)
            print(f"  Deleted: {code}")
        except Exception as e:
            print(f"  Could not delete {code}: {e}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    try:
        env = B1Environment.load(strict=True)
    except Exception as e:
        print(f"Configuration error: {e}")
        return

    with B1Client(env.config) as client:
        demo_crud(client)
        demo_run_no_params(client)
        demo_run_with_params(client)
        demo_run_stream(client)
        demo_to_pydantic(client)
        demo_error_handling(client)

    asyncio.run(demo_async(env))

    with B1Client(env.config) as client:
        cleanup(client)

    print(f"\n{'═' * 70}")
    print("  All SQL Queries scenarios completed.")
    print(f"{'═' * 70}\n")


if __name__ == "__main__":
    main()
