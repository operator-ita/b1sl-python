"""
Example 11: Service Call Interaction Patterns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Demonstrates the 3 styles of interaction supported by the SDK:
1. Pythonic (using F constants) - THE PREFERRED WAY
2. Hybrid (Mixed F and Strings) - For UDFs
3. SAP-Pure (Raw Strings)        - For copy-pasting API docs
"""
import sys
from pathlib import Path

# Add project roots to sys.path for standalone script execution
sys.path.append(str(Path(__file__).parent.parent / "src"))
sys.path.append(str(Path(__file__).parent))

from utils import use_sap_b1

from b1sl.b1sl import entities as en
from b1sl.b1sl import fields
from b1sl.b1sl.resources.base import ODataQuery
from b1sl.b1sl.resources.odata import F


def main():
    with use_sap_b1("ServiceCall Interaction Patterns") as runner:
        client = runner.client
        service_calls = client.get_resource(en.ServiceCall, "ServiceCalls")

        # 0. DYNAMIC ID DISCOVERY
        runner.info("Fetching latest ServiceCall ID...")
        latest = service_calls.list(ODataQuery(
            select=[F.ServiceCall.service_call_id],
            orderby=f"{F.ServiceCall.service_call_id} desc",
            top=1
        ))

        if not latest:
            runner.error("No calls found. Using fallback ID 106611.")
            TEST_ID = 106611
        else:
            TEST_ID = latest[0].service_call_id
            runner.success(f"Discovered TEST_ID: {TEST_ID}")

        # PATTERN 1: PYTHONIC MODE (THE GOLD STANDARD)
        runner.header("Pattern 1: Pythonic (F Constants)")
        runner.info("Best for Type Safety and IDE Autocomplete.")

        sc_f = service_calls.get(
            TEST_ID,
            select=[fields.ServiceCall.subject, fields.ServiceCall.customer_code],
            expand={
                fields.ServiceCall.business_partner: [fields.BusinessPartner.card_code],
                fields.ServiceCall.item:             [fields.Item.item_code, fields.Item.item_name]
            }
        )

        bp_code = sc_f.business_partner.card_code if sc_f.business_partner else "N/A"
        runner.result("Subject", sc_f.subject)
        runner.result("BP Code", bp_code)
        runner.result("Item Name", sc_f.item.item_name if sc_f.item else "N/A")

        # PATTERN 2: HYBRID MODE (UDF SUPPORT)
        runner.header("Pattern 2: Hybrid (F + Raw Strings)")
        runner.info("Best for queries involving User Defined Fields (U_UDF).")

        sc_mix = service_calls.get(
            TEST_ID,
            select=[fields.ServiceCall.subject, "U_OTFecha"],
            expand={
                "BusinessPartner": ["CardCode"],
                fields.ServiceCall.item: ["ItemCode", "ItemName"]
            }
        )
        runner.result("Subject", sc_mix.subject)
        runner.result("UDF 'U_OTFecha'", sc_mix.get("U_OTFecha", "None"))

        # PATTERN 3: SAP-PURE STYLE (RAW ODATA)
        runner.header("Pattern 3: SAP-Pure (Raw Strings)")
        runner.info("Best for porting existing OData snippets directly.")

        sc_sap = service_calls.get(
            TEST_ID,
            select=["Subject", "CustomerCode"],
            expand=["BusinessPartner($select=CardCode)", "Item($select=ItemCode,ItemName)"]
        )
        runner.result("Subject", sc_sap.subject)
        runner.result("Customer", sc_sap.customer_code)

        # COLLECTION PATTERN
        runner.header("Collection Pattern (LIST + Expand)")
        runner.info("Fetching the last 3 calls with their BusinessPartners in one request.")

        query = ODataQuery(
            select=[fields.ServiceCall.subject, fields.ServiceCall.service_call_id],
            expand={fields.ServiceCall.business_partner: [fields.BusinessPartner.card_code]},
            top=3
        )
        for call in service_calls.list(query):
             bp = call.business_partner.card_code if call.business_partner else "Unknown"
             print(f"  [#{call.service_call_id:<8}] ({bp:<20}) {call.subject[:40]}...")

if __name__ == "__main__":
    main()
