"""
Example 03: Asynchronous Client & Async Fluent Queries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This example demonstrates:
1. Using AsyncB1Client with 'async with'.
2. Executing multiple requests concurrently with asyncio.gather.
3. Using the new Async Fluent Query Builder.
"""
import asyncio
import sys
from pathlib import Path

# Add project roots to sys.path for standalone script execution
sys.path.append(str(Path(__file__).parent.parent / "src"))

from b1sl.b1sl import AsyncB1Client, B1Environment
from b1sl.b1sl.logging_utils import setup_logging
from b1sl.b1sl.resources.odata import F


async def main():
    setup_logging()
    env = B1Environment.load()

    # 1. Async Context Manager
    async with AsyncB1Client(env.config) as b1:
        
        # 2. Sequential Async Query (Fluent)
        print("🔍 [Async] Fetching top deudores...")
        results = await (
            b1.business_partners
            .select(F.BusinessPartner.card_code, F.BusinessPartner.current_account_balance)
            .filter(F.BusinessPartner.current_account_balance > 1000)
            .top(3)
            .execute()
        )
        
        for bp in results:
            print(f"  → {bp.card_code}: {bp.current_account_balance}")

        # 3. Concurrent Requests (Performance)
        item_codes = ["A0001", "A0002", "A0003"]
        print(f"\n🚀 Fetching {len(item_codes)} items concurrently...")
        
        # We launch multiple .get() calls simultaneously
        tasks = [b1.items.get(code) for code in item_codes]
        items = await asyncio.gather(*tasks, return_exceptions=True)

        for res in items:
            if isinstance(res, Exception):
                print(f"  ❌ Error: {res}")
            else:
                print(f"  ✨ Item: {res.item_name} ({res.item_code})")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
