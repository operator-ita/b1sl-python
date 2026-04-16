"""
Example 16: Asynchronous CRUD Operations (Create, Read, Update, Delete).

This script demonstrates the full lifecycle of a Business Partner (Customer)
using the AsyncB1Client. This is the recommended pattern for web apps
(FastAPI, Django) and high-performance integrations.
"""
import asyncio
import sys
import uuid
from pathlib import Path

# ── Path hack ───────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from b1sl.b1sl import AsyncB1Client, B1Environment
from b1sl.b1sl import entities as en
from b1sl.b1sl.exceptions import B1Exception


async def main():
    # ── 1. Load Configuration ───────────────────────────────────────────────
    try:
        env = B1Environment.load(strict=True)
        print("✅ Environment loaded successfully.")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return

    # Generate a unique CardCode for this test run
    card_code = f"ASYNC_{uuid.uuid4().hex[:6].upper()}"
    
    # ── 2. CRUD Lifecycle ──────────────────────────────────────────────────
    print(f"\n🚀 Starting Asynchronous CRUD for {card_code}\n")

    async with AsyncB1Client(env.config) as b1:
        
        # ────────── [ CREATE ] ──────────
        print("1. 🟡 [POST] Creating Business Partner...")
        new_bp = en.BusinessPartner(
            card_code=card_code,
            card_name="Async Test Partner",
            federal_tax_id="XAXX010101000",
            card_type=en.BoCardTypes.cCustomer
        )

        try:
            created = await b1.business_partners.create(new_bp)
            print(f"   ✅ Created: {created.card_code} (ETag: {created.etag})")
        except B1Exception as e:
            print(f"   ❌ Create failed: {e}")
            return

        # ────────── [ READ ] ──────────
        print("\n2. 🟡 [GET] Reading Business Partner...")
        try:
            item = await b1.business_partners.get(card_code)
            print(f"   ✅ Read Name: {item.card_name}")
        except B1Exception as e:
            print(f"   ❌ Read failed: {e}")

        # ────────── [ UPDATE ] ──────────
        print("\n3. 🟡 [PATCH] Updating Business Partner (Surgical Delta)...")
        # Construct a new minimal object for the update
        patch_data = en.BusinessPartner(
            card_name="Async Test Partner - UPDATED",
            email_address="async.test@example.com"
        )
        
        try:
            await b1.business_partners.update(card_code, patch_data)
            # Verify the update
            updated_item = await b1.business_partners.get(card_code)
            print(f"   ✅ Update verified. New Name: {updated_item.card_name}")
        except B1Exception as e:
            print(f"   ❌ Update failed: {e}")

        # ────────── [ DELETE ] ──────────
        print("\n4. 🟡 [DELETE] Removing Business Partner...")
        try:
            await b1.business_partners.delete(card_code)
            print("   ✅ Deleted successfully.")
        except B1Exception as e:
            print(f"   ❌ Delete failed: {e}")

        # ────────── [ VERIFY ] ──────────
        exists = await b1.business_partners.exists(card_code)
        if not exists:
            print("\n✅ CRUD verification complete: Resource no longer exists.")
        else:
            print("\n⚠️ CRUD verification failed: Resource still exists!")

if __name__ == "__main__":
    asyncio.run(main())
