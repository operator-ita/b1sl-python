import asyncio
import sys
from pathlib import Path

# Add project roots to sys.path for standalone script execution
sys.path.append(str(Path(__file__).parent.parent / "src"))
sys.path.append(str(Path(__file__).parent))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from b1sl.b1sl import AsyncB1Client, B1Environment, B1Config
from b1sl.b1sl.logging_utils import setup_logging
from b1sl.b1sl.models.base import B1Model

class MockItem(B1Model):
    """Simple model for demonstration purposes."""
    ItemCode: str | None = None
    ItemName: str | None = None

async def main():
    """
    This example demonstrates the 'Dry Run' (Safety Mode) functionality.
    
    Dry Run mode intercepts any write operations (POST, PATCH, DELETE) and 
    simulates a successful response (204 No Content) without sending the 
    actual request to the SAP Service Layer.
    """
    # 0. Initialize structured logging to see interception messages
    setup_logging()

    # 1. Load configuration
    env = B1Environment.load()
    config = env.config
    config.ssl_verify = False # Disable SSL verification for demo if using self-signed certs

    print(f"✅ Starting Dry Run demonstration on {config.base_url}...")

    # --- CASE 1: Global Interception via Config ---
    print("\n--- CASE 1: Global Dry Run (config.dry_run = True) ---")
    config.dry_run = True
    
    async with AsyncB1Client(config) as b1:
        # Access a dynamic resource using our simple model
        items_resource = b1.get_resource(MockItem, "Items")
        
        print("🚀 Attempting to update an Item (will be intercepted)...")
        # Update returns None, so it's safe even in dry run
        await items_resource.update("A0001", MockItem(ItemName="Safety Test"))
        print("  ✨ Intercepted: Check the INFO logs above for '[DRY RUN] Intercepting'")

        # Note: 'create' expects a response body to return the new object.
        # In Dry Run (204 No Content), this will raise a validation error
        # because result.data is None.
        print("\n🚀 Attempting to create an Item (dry run returns 204 No Content)...")
        try:
            await items_resource.create(MockItem(ItemCode="DRY-RUN", ItemName="Test"))
        except Exception as e:
            print(f"  ℹ️  Create 'failed' as expected because 204 response has no body to parse: {type(e).__name__}")

    # --- CASE 2: Context Manager (Surgical/Temporary) ---
    print("\n--- CASE 2: Context Manager (Safe/Temporary blocks) ---")
    config.dry_run = False # Global OFF
    
    async with AsyncB1Client(config) as b1:
        items_resource = b1.get_resource(MockItem, "Items")

        # We want to test an update safely without modifying SAP data
        with b1.dry_run():
            print("🚀 Updating Item inside dry_run() block...")
            await items_resource.update("A0001", MockItem(ItemName="Temporary Name Change"))
            print(f"  ✨ Intercepted: PATCH request captured (see logs above)")

        # Outside the block, the client returns to its original state
        print("  🔓 dry_run block finished. Client returned to real execution mode.")

        # --- CASE 3: Guarded Override ---
        # If global dry_run is ON for safety, you can force a real operation
        print("\n--- CASE 3: Forcing real execution with dry_run(enabled=False) ---")
        config.dry_run = True # Global ON
        
        # We need a new client or update the ContextVar directly, 
        # but the context manager is designed for this!
        async with AsyncB1Client(config) as b1_safe:
            print("🚀 Attempting a real operation while bypassing the global lock...")
            with b1_safe.dry_run(enabled=False):
                # This request WOULD reach SAP if we called a write method here
                # We'll just do a GET to show it works, but the CM would allow PATCH/POST too.
                await b1_safe.items.get("A0001")
                print("  ✅ Real execution permitted inside this block.")

    print("\n✅ Demonstration finished.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
