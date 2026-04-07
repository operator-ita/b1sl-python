"""
Refactored Document & Navigation Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Demonstrates how to fetch complex documents (Invoices) and seamlessly 
navigate to associated entities (BusinessPartners) using the SDK's typed models.
"""
import sys
from pathlib import Path
# Add project roots to sys.path for standalone script execution
sys.path.append(str(Path(__file__).parent.parent / "src"))
sys.path.append(str(Path(__file__).parent))

from b1sl.b1sl import fields as F
from b1sl.b1sl.resources.base import ODataQuery
from utils import use_sap_b1

def main():
    with use_sap_b1("Document Navigation (Invoice -> BP)") as runner:
        client = runner.client
        
        # 1. DYNAMIC DISCOVERY
        runner.header("Dynamic Document Discovery")
        runner.info("Fetching the latest Invoice with its BusinessPartner...")
        
        query = ODataQuery(
            select=[
                F.Document.doc_entry, 
                F.Document.doc_num, 
                F.Document.doc_total, 
                F.Document.doc_currency
            ],
            expand={
                F.Document.business_partner: [
                    F.BusinessPartner.card_code, 
                    F.BusinessPartner.card_name,
                    F.BusinessPartner.current_account_balance
                ]
            },
            orderby=f"{F.Document.doc_entry} desc",
            top=1
        )
        
        results = client.invoices.list(query)
        
        if not results:
            runner.error("No invoices found in this environment.")
            return
            
        invoice = results[0]
        runner.success(f"Latest Invoice Found: #{invoice.doc_num}")

        # 2. DOCUMENT DETAILS
        runner.header("Document Attribute Access")
        runner.result("Doc Entry (ID)", invoice.doc_entry)
        runner.result("Total Amount", f"{invoice.doc_total} {invoice.doc_currency}")

        # 3. SEAMLESS NAVIGATION
        runner.header("Navigation to BusinessPartner")
        if invoice.business_partner:
            bp = invoice.business_partner
            runner.info("Accessing BP data directly from the invoice object...")
            runner.result("BP Code", bp.card_code)
            runner.result("BP Name", bp.card_name)
            runner.result("BP Balance", bp.current_account_balance)
        else:
            runner.error("BusinessPartner data was not expanded or is missing.")

if __name__ == "__main__":
    main()
