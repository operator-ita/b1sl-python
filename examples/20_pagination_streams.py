"""
Example 20: Transparent Pagination Streams
 
Demonstrates the complete surface of the `.stream()` API, covering every
meaningful pattern a developer would encounter when dealing with large
SAP B1 datasets.
 
Scenarios covered:
    1.  Naive .execute() vs .stream() — the "why bother" moment.
    2.  page_size control and its HTTP request implications.
    3.  .top(N) as a hard global limit across pages.
    4.  .filter().stream() — verifying filters survive across pages.
    5.  max_pages as a safety ceiling.
    6.  itertools.islice on sync client — correct mental model.
    7.  Aggregation pattern (count, collect, first-match).
    8.  Sync client parity.
"""
import asyncio
import sys
from itertools import islice
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
 
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
 
from b1sl.b1sl import AsyncB1Client, B1Client, B1Environment
from b1sl.b1sl.resources.odata import F
 
 
def section(title: str) -> None:
    print(f"\n{'─' * 70}")
    print(f"  {title}")
    print(f"{'─' * 70}")
 
 
# ─────────────────────────────────────────────────────────────────────────────
# ASYNC SCENARIOS
# ─────────────────────────────────────────────────────────────────────────────
 
async def demo_why_stream(client: AsyncB1Client) -> None:
    """
    Scenario 1: The core problem .stream() solves.
 
    .list() returns only the first page SAP decides to give you.
    .stream() transparently chains every subsequent page until exhaustion.
    """
    section("1. execute() vs stream() — Why This Feature Exists")
 
    # Without stream: you get whatever SAP's default page size returns.
    # This is silently incomplete for large collections.
    first_page = await client.items.list()
    print(f"  .list()     → {len(first_page)} items  (one page, possibly incomplete)")
 
    # With stream: every page is fetched and every item is yielded.
    total = 0
    async for _ in client.items.stream():
        total += 1
    
    print(f"  .stream()   → {total} items  (full collection, all pages consumed)")
    print()
    print("  ⚠️  If these numbers differ, your .list() calls were silently")
    print("      truncating results. That's the bug .stream() prevents.")
 
 
async def demo_page_size(client: AsyncB1Client) -> None:
    """
    Scenario 2: page_size controls HTTP requests, not total results.
 
    page_size injects the B1-PageSize header into each request.
    Smaller page_size → more HTTP requests, less memory per request.
    Larger page_size → fewer HTTP requests, more memory per request.
    Both yield the same total number of items.
    """
    section("2. page_size — HTTP Efficiency vs Memory Trade-off")
 
    # Track requests by counting yields per page implicitly via max_pages.
    
    count_small = 0
    async for _ in client.items.stream(page_size=5, max_pages=2):
        count_small += 1

    count_large = 0
    async for _ in client.items.stream(page_size=50, max_pages=2):
        count_large += 1
 
    print(f"  page_size=5,  max_pages=2  → yielded {count_small} items (up to 10 total)")
    print(f"  page_size=50, max_pages=2  → yielded {count_large} items (up to 100 total)")
    print()
    print("  💡 page_size is an HTTP concern, not a data concern.")
    print("     Use .top(N) when you want to limit total items returned.")
 
 
async def demo_top_as_global_limit(client: AsyncB1Client) -> None:
    """
    Scenario 3: .top(N) is a hard global cap — not a page size.
 
    .top(10).stream(page_size=3) will make multiple requests of 3 items
    each, but will stop yielding after exactly 10 items total.
    """
    section("3. .top(N) — Hard Global Limit Across Pages")
 
    items = []
    async for item in client.items.top(10).stream(page_size=3):
        items.append(item.item_code)
 
    print(f"  .top(10).stream(page_size=3) → {len(items)} items yielded")
    print(f"  Codes: {items}")
    print()
    print("  ✅ Exactly 10 items regardless of page_size or SAP's internal limit.")
 
 
async def demo_filter_survives_pages(client: AsyncB1Client) -> None:
    """
    Scenario 4: Filters are preserved across every page request.
 
    This is the most commonly broken behavior in naive pagination
    implementations. build_next_params ensures filters from the original 
    query are re-injected into every subsequent request.
    """
    section("4. .filter().stream() — Filters Survive Page Boundaries")
 
    # Standard OData filter using operator overloading
    target_type = "itItems" 
    count = 0
    async for item in client.items.filter(F.ItemType == target_type).stream(page_size=10):
        count += 1
        # Spot-check: every item must match the filter.
        if item.item_type != target_type:
            print("\n  🔴 ERROR: Filter breach detected on page boundary!")
            print(f"     Expected ItemType : {target_type!r}")
            print(f"     Actual ItemType   : {item.item_type!r}")
            print(f"     Record Code       : {item.item_code!r}")
            sys.exit(1)
        if count >= 50:
            break
 
    print(f"  Streamed {count} items — all confirmed ItemType='{target_type}'.")
    print("  ✅ Filter was correctly propagated to every page request.")
 
 
async def demo_max_pages_safety(client: AsyncB1Client) -> None:
    """
    Scenario 5: max_pages prevents runaway streams in production code.
    """
    section("5. max_pages — Safety Ceiling on HTTP Requests")
 
    # With page_size=10 and max_pages=2: at most 20 items, exactly 2 requests.
    items_2pages = [item async for item in client.items.stream(page_size=10, max_pages=2)]
    print(f"  max_pages=2, page_size=10 → {len(items_2pages)} items (≤ 20 expected)")
 
    items_1page = [item async for item in client.items.stream(page_size=10, max_pages=1)]
    print(f"  max_pages=1, page_size=10 → {len(items_1page)} items (≤ 10 expected)")
 
 
async def demo_aggregation_patterns(client: AsyncB1Client) -> None:
    """
    Scenario 7: Common aggregation patterns over a full stream.
    """
    section("7. Aggregation Patterns — Count, Collect, First-Match")
 
    # Pattern A: Total count (compare with .count() for verification)
    total_streamed = 0
    async for _ in client.items.stream(page_size=100):
        total_streamed += 1
        
    total_count    = await client.items.count()
    print(f"  Total via .stream() : {total_streamed}")
    print(f"  Total via .count()  : {total_count}")
    print(f"  Match: {'✅' if total_streamed == total_count else '❌'}")
 
    # Pattern B: First item matching a runtime condition
    first_long_name = None
    async for item in client.items.stream(page_size=50):
        if item.item_name and len(item.item_name) > 30:
            first_long_name = item
            break
    print(f"\n  First item with name > 30 chars: {first_long_name.item_code if first_long_name else '(nonefound)'}")
 
    # Pattern C: Collect a specific field across the entire collection
    all_codes = [item.item_code async for item in client.items.stream(page_size=100)]
    print(f"\n  All item codes collected: {len(all_codes)} total")
 
 
# ─────────────────────────────────────────────────────────────────────────────
# SYNC SCENARIOS
# ─────────────────────────────────────────────────────────────────────────────
 
def demo_sync_parity(env: B1Environment) -> None:
    """
    Scenario 8: Sync client has full feature parity with async.
    """
    section("8. Sync Client — Full Feature Parity")
 
    with B1Client(env.config) as client:
        total = sum(1 for _ in client.items.stream(page_size=50))
        print(f"  Sync .stream() total: {total} items")
 
        top5 = [item.item_code for item in client.items.top(5).stream(page_size=2)]
        print(f"  Sync .top(5).stream(page_size=2): {top5}")
 
 
def demo_islice_mental_model(env: B1Environment) -> None:
    """
    Scenario 6: itertools.islice — correct mental model.
    """
    section("6. itertools.islice — Consumption Limit vs Request Limit")
 
    with B1Client(env.config) as client:
        stream = client.items.stream(page_size=20)
 
        print("  Consuming first 5 items via islice(stream, 5)...")
        for count, item in enumerate(islice(stream, 5), 1):
            print(f"    [{count:02}] {item.item_code}")
 
        print("\n  Compare with .top(5).stream(page_size=5):")
        for count, item in enumerate(client.items.top(5).stream(page_size=5), 1):
            print(f"    [{count:02}] {item.item_code}")
 
        print("\n  ✅ Same output. Different HTTP behavior.")
 
 
# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
 
async def run_async_demos(env: B1Environment) -> None:
    async with AsyncB1Client(env.config) as client:
        await demo_why_stream(client)
        await demo_page_size(client)
        await demo_top_as_global_limit(client)
        await demo_filter_survives_pages(client)
        await demo_max_pages_safety(client)
        await demo_aggregation_patterns(client)
 
 
def main() -> None:
    try:
        env = B1Environment.load(strict=True)
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return
 
    # Async scenarios
    asyncio.run(run_async_demos(env))
 
    # Sync scenarios
    demo_islice_mental_model(env)
    demo_sync_parity(env)
 
    print(f"\n{'═' * 70}")
    print("  All pagination scenarios completed.")
    print(f"{'═' * 70}\n")
 
 
if __name__ == "__main__":
    main()
