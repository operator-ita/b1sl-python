"""
Example 04: Fluent OData Queries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This example demonstrates the modern Fluent Query Builder API.
Instead of passing strings or ODataQuery objects, you can chain
methods for a type-safe experience.
"""
import sys
from pathlib import Path

# Add project roots to sys.path for standalone script execution
sys.path.append(str(Path(__file__).parent.parent / "src"))

from b1sl.b1sl import B1Client, B1Environment
from b1sl.b1sl import fields as F
from b1sl.b1sl.logging_utils import setup_logging


def main():
    setup_logging()
    env = B1Environment.load()

    with B1Client(env.config) as b1:
        print("🔍 Searching for top 3 customers with debt using Fluent API...")

        # CHAINING: select -> filter -> orderby -> top -> execute
        results = (
            b1.business_partners
            .select(F.BusinessPartner.card_code, F.BusinessPartner.card_name, F.BusinessPartner.current_account_balance)
            .filter(F.BusinessPartner.current_account_balance > 0)
            .orderby(F.BusinessPartner.current_account_balance, desc=True)
            .top(3)
            .execute()
        )

        for bp in results:
            print(f"💰 {bp.card_code}: {bp.card_name:<30} | Balance: {bp.current_account_balance:>10}")


        print("\n🔍 Complex Item Filtering Example...")
        
        # Searching for Items with stock and certain naming pattern
        stocked_items = (
            b1.items
            .select(F.Item.item_code, F.Item.item_name, F.Item.on_hand)
            .filter((F.Item.on_hand > 5) & (F.Item.item_name.contains("QUESO")))
            .top(5)
            .execute()
        )

        if not stocked_items:
            print("📝 No items match the 'QUESO' filter with stock > 5.")
        else:
            for item in stocked_items:
                print(f"📦 {item.item_code}: {item.item_name} ({item.on_hand} in stock)")

if __name__ == "__main__":
    main()
