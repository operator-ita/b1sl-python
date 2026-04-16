"""
Example: Robust Error Handling in SAP B1 Service Layer.

This script demonstrates how to catch and handle common exceptions provided by the SDK,
ensuring your integration stays resilient when resources are missing or data is invalid.
"""
import sys
from pathlib import Path

# ── Path hack ───────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from b1sl.b1sl import B1Client, B1Environment
from b1sl.b1sl import entities as en
from b1sl.b1sl.exceptions import (
    B1Exception,
    B1NotFoundError,
    B1ValidationError,
)


def main():
    # 1. Load configuration from .env
    try:
        env = B1Environment.load(strict=True)
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return

    # 2. Use B1Client context manager
    with B1Client(env.config) as b1:
        
        # ─── CASE 1: Handling Missing Resources (404) ───
        print("\n🔍 Case 1: Fetching a non-existent Business Partner...")
        non_existent_code = "NONEXISTENT"
        
        try:
            bp = b1.business_partners.get(non_existent_code)
            print(f"✅ Found: {bp.card_name}")
        except B1NotFoundError:
            print(f"ℹ️ Expected: B1NotFoundError caught. BP '{non_existent_code}' does not exist.")
        except B1Exception as e:
            print(f"❌ Unexpected SAP error: {e}")

        # ─── CASE 2: Using the .exists() helper ───
        print("\n🔎 Case 2: Using the .exists() method...")
        if b1.business_partners.exists(non_existent_code):
            print("⚠️ Logic Error: It says it exists but it shouldn't.")
        else:
            print(f"✅ Success: .exists() returned False for '{non_existent_code}'.")

        # ─── CASE 3: Handling Validation Errors (400) ───
        print("\n🚫 Case 3: Attempting to create an invalid Business Partner...")
        # Creation without mandatory CardCode should trigger a 400 Validation Error
        invalid_bp = en.BusinessPartner(card_name="I have no code")
        
        try:
            b1.business_partners.create(invalid_bp)
        except B1ValidationError as e:
            print("ℹ️ Expected: B1ValidationError caught.")
            print(f"   Message: {e}")
            print(f"   Raw Detail (for inspection): {e.details}")
        except B1Exception as e:
             print(f"❌ Unexpected SAP error: {e}")

        # ─── CASE 4: Understanding Concurrency (412) ───
        print("\n🔄 Case 4: Optimistic Concurrency (Information)...")
        print("   If another process changes a Business Partner between your GET and PATCH,")
        print("   the SDK will raise a SAPConcurrencyError. Here is how you should catch it:")
        print("""
        try:
            b1.business_partners.update(card_code, surgical_delta)
        except SAPConcurrencyError as e:
            print(f"Conflict on {e.endpoint}! Re-fetch, merge and retry.")
        """)

    print("\n✅ Error handling demonstration complete.")

if __name__ == "__main__":
    main()
