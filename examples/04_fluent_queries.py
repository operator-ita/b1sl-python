"""
Example 04: Fluent OData Queries (Dynamic vs Static)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This example demonstrates the two ways to build OData queries in the SDK:
1. The "Elite" Dynamic F Proxy (Zero-import, uses SAP CamelCase names)
2. The "Pythonic" Static Constants (Autocomplete, uses snake_case names)
"""
import sys
from pathlib import Path

# Add project roots to sys.path for standalone script execution
sys.path.append(str(Path(__file__).parent.parent / "src"))

from b1sl.b1sl import (
    B1Client,
    B1Environment,  # Static Field Constants
)
from b1sl.b1sl.logging_utils import setup_logging
from b1sl.b1sl.resources.odata import F  # Dynamic Field Proxy


def main():
    setup_logging()
    env = B1Environment.load()

    with B1Client(env.config) as b1:
        # --- PATTERN 1: The "Elite" Dynamic F Proxy ---
        # Pros: No sub-imports, supports UDFs natively.
        # Cons: No IDE autocomplete, requires knowing SAP field names (CamelCase).
        print("\n🚀 Pattern 1: Dynamic F Proxy (SAP Names)")
        
        results = (
            b1.business_partners
            .select(F.CardCode, F.CardName, F.CurrentAccountBalance)
            .filter(F.CurrentAccountBalance > 0)
            .top(3)
            .execute()
        )

        for bp in results:
            print(f"💰 {bp.card_code}: {bp.card_name:<20} | Balance: {bp.current_account_balance:>10}")


        # --- PATTERN 2: The "Pythonic" Static Constants ---
        # Pros: Full IDE autocomplete, type-safe discovery, uses snake_case.
        # Cons: Requires importing specific field classes (e.g. fields.Item).
        print("\n🐍 Pattern 2: Static Constants ( snake_case + Autocomplete)")
        
        from b1sl.b1sl.fields import Item

        stocked_items = (
            b1.items
            .select(Item.item_code, Item.item_name, Item.on_hand)
            .filter((Item.on_hand > 5) & (Item.item_name.contains("A")))
            .top(3)
            .execute()
        )

        for item in stocked_items:
            print(f"📦 {item.item_code}: {item.item_name} ({item.on_hand} in stock)")


        # --- COMPOSITION: Best of Both Worlds ---
        # You can mix them. Use Static for common fields and F for deep paths or UDFs.
        print("\n🧩 Pattern 3: Composite Access")
        
        # Accessing a nested property using F for the path
        q = (
            b1.items
            .select(Item.item_code, F.ItemWarehouseInfoCollection / F.WarehouseCode)
            .top(1)
            .execute()
        )
        print(f"✅ Composite Query Executed for {len(q)} item(s).")

if __name__ == "__main__":
    main()
