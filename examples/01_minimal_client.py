"""
Example 01: Minimal Client & Basic CRUD
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This example demonstrates the most basic usage of the B1Client:
1. Loading configuration from the environment.
2. Initializing the client.
3. Fetching a single entity (GET).
4. Listing entities with basic parameters.
"""
import os
import sys
from pathlib import Path

# Add project roots to sys.path for standalone script execution
sys.path.append(str(Path(__file__).parent.parent / "src"))

from b1sl.b1sl import B1Client, B1Environment
from b1sl.b1sl.logging_utils import setup_logging


def main():
    # 1. Initialize logging (Dev mode by default)
    setup_logging()

    # 2. Load environment configuration
    # Requires B1SL_BASE_URL, B1SL_USERNAME, etc. in .env or environment
    env = B1Environment.load()
    
    print(f"✅ Connecting to {env.config.base_url}...")

    # 3. Use B1Client as a context manager (handles login/logout automatically)
    with B1Client(env.config) as b1:
        
        # 4. Fetch a Business Partner (GET)
        # We'll try to find any code, or use a default
        card_code = os.getenv("TEST_CARD_CODE", "C20000")
        
        print(f"\n🔍 Fetching Business Partner: {card_code}...")
        try:
            bp = b1.business_partners.get(card_code)
            print(f"✨ Found: {bp.card_name} (Balance: {bp.current_account_balance})")
        except Exception as e:
            print(f"❌ Could not fetch {card_code}: {e}")

        # 5. List Items (Basic)
        print("\n🚀 Listing first 5 items...")
        items = b1.items.top(5).execute()
        
        for item in items:
            print(f"  - {item.item_code}: {item.item_name}")

if __name__ == "__main__":
    main()
