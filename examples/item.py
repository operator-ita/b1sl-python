"""
Refactored Item Example (Modern SDK Patterns)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Demonstrates dynamic ID fetching, calculated properties, 
and advanced OData filtering using the new entity architecture.
"""
import sys
from pathlib import Path
# Add project roots to sys.path for standalone script execution
sys.path.append(str(Path(__file__).parent.parent / "src"))
sys.path.append(str(Path(__file__).parent))

from b1sl.b1sl import entities as en, fields as F
from b1sl.b1sl.resources.base import ODataQuery
from utils import use_sap_b1

def main():
    with use_sap_b1("Item Inventory & Stock Patterns") as runner:
        client = runner.client
        
        # 1. FETCHING DYNAMICALLY
        runner.header("Dynamic Item Discovery")
        runner.info("Finding an item with physical stock...")
        
        items = client.items.list(ODataQuery(
            filter=f"{F.Item.quantity_on_stock} gt 0",
            top=1,
            select=[F.Item.item_code]
        ))
        
        if not items:
            runner.error("No stocked items found. Checking fallback.")
            test_id = runner.test_data.get_test_item("simple") or "7500473003377"
        else:
            test_id = items[0].item_code
            runner.success(f"Dynamic ID Identified: {test_id}")

        # 2. DETAILED ENTITY RETRIEVAL (GET)
        runner.header("Individual Entity Detail (GET)")
        item = client.items.get(test_id)
        
        runner.result("Item Code", item.item_code)
        runner.result("Item Name", item.item_name)
        runner.result("Physical Stock", item.quantity_on_stock)
        runner.result("Available (Calculated)", item.available_stock) # Logic: OnHand - Committed + Ordered

        # 3. ADVANCED ODATA FILTERING (LIST)
        runner.header("Advanced OData Filtering (LIST)")
        runner.info("Searching for items using complex criteria...")
        
        filter_expr = (
            f"({F.Item.quantity_on_stock} gt 0) and "
            f"(contains({F.Item.item_name}, 'QUESO') or "
            f" {F.Item.update_date} ge '2024-01-01')"
        )
        
        results = client.items.list(ODataQuery(
            filter=filter_expr,
            top=5,
            select=[F.Item.item_code, F.Item.item_name]
        ))
        
        for idx, it in enumerate(results, 1):
             print(f"  [{idx}] {it.item_code:<15} | {it.item_name}")

        # 4. UPDATING (CONSTRUCTION & PAYLOAD)
        runner.header("Mutation Preparation (Pydantic Models)")
        runner.info("Constructing update payload using snake_case model...")
        
        update_model = en.Item(
            item_name="QUESO OAXACA PREMIUM (CORRECION)",
            valid=True
        )
        runner.result("Generated JSON", update_model.to_api_payload())

if __name__ == "__main__":
    main()

