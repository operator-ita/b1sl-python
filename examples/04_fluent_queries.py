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

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

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
        # --- PATTERN 1 (RECOMMENDED): The "Pythonic" Static Constants ---
        # Pros: Full IDE autocomplete, metadata-verified SAP names, typo-safe
        #       (a typo raises AttributeError before any HTTP request).
        print("\n🐍 Pattern 1: Static Constants (snake_case + Autocomplete)")

        from b1sl.b1sl.fields import BusinessPartner, Item

        results = (
            b1.business_partners
            .select(BusinessPartner.card_code, BusinessPartner.card_name,
                    BusinessPartner.current_account_balance)
            .filter(BusinessPartner.current_account_balance > 0)
            .top(3)
            .execute()
        )

        for bp in results:
            print(f"💰 {bp.card_code}: {bp.card_name:<20} | Balance: {bp.current_account_balance:>10}")

        stocked_items = (
            b1.items
            .select(Item.item_code, Item.item_name, Item.quantity_on_stock)
            .filter((Item.quantity_on_stock > 5) & (Item.item_name.contains("A")))
            .top(3)
            .execute()
        )

        for item in stocked_items:
            print(f"📦 {item.item_code}: {item.item_name} ({item.quantity_on_stock} in stock)")


        # --- PATTERN 2: The Dynamic F Proxy (UDFs / raw names) ---
        # F is a raw passthrough with no validation — its legitimate use is
        # UDFs (U_*), which are not in $metadata so no constant exists.
        print("\n🚀 Pattern 2: Dynamic F Proxy (raw SAP names — UDFs)")

        balance_check = (
            b1.business_partners
            .select(F.CardCode)          # raw SAP name, passed verbatim
            .filter(F.CurrentAccountBalance > 0)
            .top(1)
            .execute()
        )
        print(f"✅ F proxy query executed for {len(balance_check)} partner(s).")


        # --- COMPOSITION: Best of Both Worlds ---
        # You can mix them. Use Static for common fields and F for deep paths or UDFs.
        print("\n🧩 Pattern 3: Composite Access")
        
        # Selecting a complex-type collection property alongside scalar fields.
        # (Path syntax like Coll/Field only works on navigation properties —
        # ItemWarehouseInfoCollection is a complex collection, so select it whole.)
        q = (
            b1.items
            .select(Item.item_code, F.ItemWarehouseInfoCollection)
            .top(1)
            .execute()
        )
        print(f"✅ Composite Query Executed for {len(q)} item(s).")

if __name__ == "__main__":
    main()
