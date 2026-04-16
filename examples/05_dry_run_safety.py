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

from b1sl.b1sl import AsyncB1Client, B1Environment
from b1sl.b1sl.fields import BusinessPartner as BP
from b1sl.b1sl.logging_utils import setup_logging
from b1sl.b1sl.models._generated.entities.businesspartners import BusinessPartner


async def main():
    # 0. Initialize structured logging
    setup_logging()

    # 1. Load configuration from environment/.env
    env = B1Environment.load()
    config = env.config
     
    print(f"✅ Connecting to {config.base_url} (DB: {config.company_db})...")
    print("🚀 Starting Risk Management Sync...")
    
    async with AsyncB1Client(config) as b1:
        # A. Localize the Business Partner with the highest debt
        # Using fluent orderBy and Top 1
        print("🔍 Searching for the highest debtor...")
        results = await b1.business_partners.select(
            BP.card_code, 
            BP.card_name, 
            BP.current_account_balance
        ).orderby(
            BP.current_account_balance, 
            desc=True
        ).top(1).execute()

        if not results:
            print("✅ No Business Partners found.")
            return

        debtor = results[0]
        print(f"⚠️ High risk identified: [{debtor.card_code}] {debtor.card_name}")
        print(f"💰 Current Balance: {debtor.current_account_balance}")

        # B. Deactivate the Partner using a safe 'Dry Run'
        # Notice we use the standard Python Boolean 'True'
        print("🛡️ Enabling DRY RUN for safety...")
        with b1.dry_run():
            # We only send the delta (Frozen=True)
            # This avoids 'Primary key cannot be updated' errors
            await b1.business_partners.update(
                debtor.card_code, 
                BusinessPartner(frozen=True)
            )
            print(f"✨ [DRY RUN] Request to freeze {debtor.card_code} sent successfully.")
            print("📝 No real changes were made to the SAP database.")

if __name__ == "__main__":
    # Execute the event loop
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
