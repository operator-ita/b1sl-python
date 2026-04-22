"""
Example 17: Elite Dynamic UDF Handling.

Demonstrates the most concise and professional patterns for 
handling SAP User Defined Fields (UDFs) within the SDK.
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


async def main():
    # ── 1. Load Configuration ───────────────────────────────────────────────
    try:
        env = B1Environment.load(strict=True)
        print("✅ Environment loaded successfully.")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return

    card_code = f"UD_T_{uuid.uuid4().hex[:6].upper()}"
    
    async with AsyncB1Client(env.config) as b1:
        print(f"🚀 Executing Dynamic UDF patterns for {card_code}")

        # 2. Creation with Injected UDFs
        # UDFs are passed as a dict and automatically mapped to the root payload.
        new_bp = en.BusinessPartner(
            card_code=card_code,
            card_name="UDF Partner",
            federal_tax_id="XAXX010101000",
            udfs={"U_CFDi_UsoCFDi": "P01"}
        )
        await b1.business_partners.create(new_bp)
        print(f"✅ Creation success: {new_bp.to_api_payload()}.")

        # 3. Surgical Delta Update (Mixed Native + UDFs)
        # This is the most efficient update pattern.
        delta = en.BusinessPartner(
            email_address="elite.udf@example.com",
            udfs={"U_CFDi_MetodoPago": "PPD"}
        )
        await b1.business_partners.update(card_code, delta)
        print(f"✅ Surgical update sent: {delta.to_api_payload()}")

        # 4. Verification & Reading
        # Access UDFs via the protected .udfs mapping proxy.
        bp = await b1.business_partners.get(card_code)
        print(f"✅ Verified: Email='{bp.email_address}'")
        updated_udfs = {k: v for k, v in bp.udfs.items()}
        print(f"   UDFs on record: {updated_udfs}")

        # 5. Cleanup
        await b1.business_partners.delete(card_code)
        print("✅ Resource deleted.")



if __name__ == "__main__":
    asyncio.run(main())
