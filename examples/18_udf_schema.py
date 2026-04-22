"""
Example 18: UDF Schema Container and Dynamic Validation.

Demonstrates the complete lifecycle of SAP User Defined Fields (UDFs):
    Discovery → Introspection → Validation → Serialization → PATCH

Covers both async and sync clients, and the new UDFSchema container.
"""
import asyncio
import sys
import uuid
from pathlib import Path

# ── Path hack ────────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from b1sl.b1sl import AsyncB1Client, B1Client, B1Environment
from b1sl.b1sl import entities as en


# ─────────────────────────────────────────────────────────────────────────────
# Helper: pretty-print a section header
# ─────────────────────────────────────────────────────────────────────────────
def section(title: str) -> None:
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")


async def main() -> None:
    # ── 1. Environment ────────────────────────────────────────────────────────
    section("1. Environment")
    try:
        env = B1Environment.load(strict=True)
        print("✅ Environment loaded.")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return

    card_code = f"UD_T_{uuid.uuid4().hex[:6].upper()}"

    async with AsyncB1Client(env.config) as b1:

        # ── 2. Create a Business Partner with UDFs ────────────────────────────
        section("2. Create Business Partner with UDFs")
        new_bp = en.BusinessPartner(
            card_code=card_code,
            card_name="UDF Demo Partner",
            federal_tax_id="XAXX010101000",
            udfs={"U_CFDi_UsoCFDi": "P01", "U_CFDi_MetodoPago": "PUE"},
        )
        await b1.business_partners.create(new_bp)
        print(f"✅ Created: {card_code}")
        print(f"   Payload sent: {new_bp.to_api_payload()}")


        # ── 3. Schema Discovery → UDFSchema container ─────────────────────────
        section("3. Schema Discovery")
        schema = await b1.business_partners.get_udf_schema()
        # schema is now a UDFSchema, not a raw list.
        print(f"✅ Retrieved schema: {schema!r}")          # UDFSchema(table='OCRD', fields=20)
        print(f"   Total UDF fields : {len(schema)}")
        print(f"   Field names      : {schema.names[:5]}...")


        # ── 4. Introspection — direct key access ──────────────────────────────
        section("4. Introspection")

        # 4a. Safe lookup — .get() returns None instead of raising KeyError
        uso_cfdi = schema.get("U_CFDi_UsoCFDi")
        if uso_cfdi:
            print(f"✅ U_CFDi_UsoCFDi → type={uso_cfdi.type}, size={uso_cfdi.size}")
        else:
            print("   U_CFDi_UsoCFDi not found in this environment.")

        # 4b. Membership test — natural Python idiom
        if "U_CFDi_MetodoPago" in schema:
            metodo = schema["U_CFDi_MetodoPago"]
            print(f"✅ U_CFDi_MetodoPago → type={metodo.type}, desc='{metodo.description}'")

        # 4c. Iteration — UDFSchema is a proper iterable
        float_fields = [u.name for u in schema if u.type == "db_Float"]
        print(f"   Float UDFs in OCRD: {float_fields or '(none)'}")


        # ── 5. Validation (opt-in) ────────────────────────────────────────────
        section("5. Opt-In Pydantic Validation")

        # Generate a Pydantic model scoped ONLY to the UDFs — no full-document inflation.
        DynamicUDFs = schema.to_pydantic_model("BusinessPartnerUDFs")
        print(f"✅ Dynamic model generated: {DynamicUDFs.__name__}")

        # 5a. Happy path
        good_data = {"U_CFDi_UsoCFDi": "P01", "U_CFDi_MetodoPago": "PPD"}
        validated = DynamicUDFs.model_validate(good_data)
        print(f"✅ Valid data accepted: {validated.model_dump(exclude_none=True)}")

        # 5b. Bad path — intentional type error to show early feedback
        # We know U_MinimoUtilidad exists and is db_Float -> float
        bad_data = {"U_CFDi_UsoCFDi": "P01", "U_MinimoUtilidad": "veinticinco"}  
        try:
            DynamicUDFs.model_validate(bad_data)
        except Exception as e:
            print("⚠️  Validation error caught before hitting SAP:")
            print(f"   {str(e).splitlines()[1] if len(str(e).splitlines()) > 1 else str(e)}")
 
 
        # ── 6. validate_and_dump — full loop shortcut ─────────────────────────
        section("6. validate_and_dump — Discover → Validate → Serialize")

        # The most ergonomic pattern: one call, SAP-ready payload out.
        # No need to know Pydantic internals.
        try:
            payload = schema.validate_and_dump(
                {"U_CFDi_UsoCFDi": "G03", "U_CFDi_MetodoPago": "PPD", "U_MinimoUtilidad": 25.5}
            )
            print(f"✅ SAP-ready payload: {payload}")
        except Exception as e:
            print(f"❌ validate_and_dump failed: {e}")
 
 
        # ── 7. Surgical PATCH using validated payload ─────────────────────────
        section("7. Surgical PATCH with validated UDFs")
 
        delta = en.BusinessPartner(
            email_address="udf.demo@example.com",
            udfs=payload,   # already validated and serialized — safe to send
        )
        await b1.business_partners.update(card_code, delta)
        print(f"✅ PATCH sent: {delta.to_api_payload()}")
 
 
        # ── 8. Verification ───────────────────────────────────────────────────
        section("8. Verification")
        item = await b1.business_partners.get(card_code)
        print(f"✅ Read back: email='{item.email_address}'")
        # Only show the fields we updated to keep the output concise
        relevant_udfs = {k: v for k, v in item.udfs.items() if k in payload}
        print(f"   UDFs stored: {relevant_udfs}")
 
 
        # ── 9. Manual table override ──────────────────────────────────────────
        section("9. Manual Table Override (cross-table introspection)")
 
        # Reuse any resource's adapter to discover UDFs of an unmapped table.
        items_schema = await b1.business_partners.get_udf_schema(table_name="OITM")
        print(f"✅ 'OITM' (Items) schema via BP resource: {items_schema!r}")
        print(f"   First 5 field names: {items_schema.names[:5]}")
 
 
        # ── 10. Cleanup ───────────────────────────────────────────────────────
        section("10. Cleanup")
        await b1.business_partners.delete(card_code)
        print(f"✅ {card_code} deleted.")
 
 
    # ── 11. Synchronous client — same API surface ─────────────────────────────
    section("11. Bonus: Synchronous Client")
    with B1Client(env.config) as b1_sync:
        schema_sync = b1_sync.business_partners.get_udf_schema()
        print(f"✅ Sync schema: {schema_sync!r}")
 
        # Every capability works identically in sync context.
        if "U_CFDi_UsoCFDi" in schema_sync:
            print(f"   U_CFDi_UsoCFDi type: {schema_sync['U_CFDi_UsoCFDi'].type}")
 
        payload_sync = schema_sync.validate_and_dump({"U_CFDi_UsoCFDi": "G03"})
        print(f"   validate_and_dump (sync): {payload_sync}")
 
    print(f"\n{'═' * 60}")
    print("  All patterns completed successfully.")
    print(f"{'═' * 60}\n")
 
 
if __name__ == "__main__":
    asyncio.run(main())
