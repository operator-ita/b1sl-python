"""
Example 15: Synchronous CRUD Operations (Create, Read, Update, Delete).

This script demonstrates the full lifecycle of a Business Partner (Customer)
using the synchronous B1Client. It follows best practices by using 
"Surgical Deltas" for updates to avoid ETag conflicts and data loss.
"""
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

from b1sl.b1sl import B1Client, B1Environment
from b1sl.b1sl import entities as en
from b1sl.b1sl.exceptions import B1Exception


def main():
    # ── 1. Load Configuration ───────────────────────────────────────────────
    try:
        env = B1Environment.load(strict=True)
        print("✅ Environment loaded successfully.")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return

    # Generate a unique CardCode for this test run
    card_code = f"SYNC_{uuid.uuid4().hex[:6].upper()}"
    
    # ── 2. CRUD Lifecycle ──────────────────────────────────────────────────
    print(f"\n🚀 Starting Synchronous CRUD for {card_code}\n")

    with B1Client(env.config) as b1:
        
        # ────────── [ CREATE ] ──────────
        print("1. 🟡 [POST] Creating Business Partner...")
        new_bp = en.BusinessPartner(
            card_code=card_code,
            card_name="Sync Test Partner",
            federal_tax_id="XAXX010101000", # 13 chars (MX RFC)
            card_type=en.BoCardTypes.cCustomer
        )

        try:
            created = b1.business_partners.create(new_bp)
            print(f"   ✅ Created: {created.card_code} (ETag: {created.etag})")
        except B1Exception as e:
            print(f"   ❌ Create failed: {e}")
            return

        # ────────── [ READ ] ──────────
        print("\n2. 🟡 [GET] Reading Business Partner...")
        try:
            item = b1.business_partners.get(card_code)
            print(f"   ✅ Read Name: {item.card_name}")
            print(f"   ✅ Read RFC:  {item.federal_tax_id}")
        except B1Exception as e:
            print(f"   ❌ Read failed: {e}")

        # ────────── [ UPDATE ] ──────────
        print("\n3. 🟡 [PATCH] Updating Business Partner (Surgical Delta)...")
        # Recommendation: Do NOT send the whole 'item' back.
        # Construct a new minimal object with only the fields you want to change.
        patch_data = en.BusinessPartner(
            card_name="Sync Test Partner - UPDATED",
            email_address="sync.test@example.com"
        )
        
        try:
            b1.business_partners.update(card_code, patch_data)
            # Verify the update with a fresh GET
            updated_item = b1.business_partners.get(card_code)
            print(f"   ✅ Update verified. New Name: {updated_item.card_name}")
        except B1Exception as e:
            print(f"   ❌ Update failed: {e}")

        # ────────── [ DELETE ] ──────────
        print("\n4. 🟡 [DELETE] Removing Business Partner...")
        try:
            b1.business_partners.delete(card_code)
            print("   ✅ Deleted successfully.")
        except B1Exception as e:
            print(f"   ❌ Delete failed: {e}")

        # ────────── [ VERIFY ] ──────────
        if not b1.business_partners.exists(card_code):
            print("\n✅ CRUD verification complete: Resource no longer exists.")
        else:
            print("\n⚠️ CRUD verification failed: Resource still exists!")

if __name__ == "__main__":
    main()
