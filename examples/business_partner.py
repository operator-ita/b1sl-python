"""
Refactored BusinessPartner Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Demonstrates how to fetch, filter, and prepare payloads for Business Partners
using the SDK's typed models and ODataQuery builder.
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
    with use_sap_b1("BusinessPartner Patterns") as runner:
        client = runner.client
        
        # 1. SIMPLE RETRIEVAL
        runner.header("Simple BusinessPartner Fetch (GET)")
        runner.info("Fetching a single record with selective fields...")
        
        test_bp = runner.test_data.get_test_bp("simple") or "C0000001"
        bp = client.business_partners.get(
            test_bp, 
            select=[F.BusinessPartner.card_code, F.BusinessPartner.card_name, F.BusinessPartner.card_type]
        )
        
        runner.result("Card Code", bp.card_code)
        runner.result("Card Name", bp.card_name)
        runner.result("Card Type", bp.card_type)

        # 2. EXPANSION (CONTACTS)
        runner.header("Expansion (Contacts Only)")
        runner.info(f"Retrieving contacts for {bp.card_code}...")
        
        bp_contacts = client.business_partners.get(
            bp.card_code, 
            select=[F.BusinessPartner.card_code, F.BusinessPartner.contact_employees]
        )
        
        contacts = bp_contacts.contact_employees or []
        runner.result("Contact Count", len(contacts))
        for ct in contacts[:3]:
             print(f"  → {ct.name:<20} | {ct.e_mail}")

        # 3. ADVANCED LISTING (ODATA)
        runner.header("Advanced Listing (OData Query)")
        runner.info("Fetching top 3 customers with outstanding balance...")
        
        query = ODataQuery(
            filter=f"{F.BusinessPartner.current_account_balance} gt 0",
            top=3,
            select=[F.BusinessPartner.card_code, F.BusinessPartner.card_name]
        )
        
        for idx, partner in enumerate(client.business_partners.list(query), 1):
             print(f"  [{idx}] {partner.card_code:<15} | {partner.card_name}")

        # 4. PAYLOAD CONSTRUCTION (FOR CREATION/UPDATE)
        runner.header("Pydantic Model Construction")
        runner.info("Preparing a creation payload using typed enums and booleans...")
        
        new_bp_model = en.BusinessPartner(
            card_code="C-SDK-TEST",
            card_name="SDK AUTOMATED PARTNER",
            card_type=en.BoCardTypes.cCustomer,
            frozen=False  # Handled as 'tNO' by SAP normalization
        )
        
        runner.result("Projected JSON", new_bp_model.to_api_payload())

if __name__ == "__main__":
    main()