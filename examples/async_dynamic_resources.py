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
from b1sl.b1sl.resources.async_base import AsyncGenericResource
from b1sl.b1sl.logging_utils import setup_logging
from b1sl.b1sl.models._generated.entities.general import Document
from b1sl.b1sl.models._generated.entities.inventory import Item

# ==============================================================================
# SUBCLASSING THE CLIENT (THE RECOMMENDED WAY FOR CUSTOM EXTENSIONS)
# ==============================================================================
# It is an excellent idea to subclass the core AsyncB1Client in your own projects
# if you want to add static type hints to endpoints we didn't include by default.
# It requires zero internal modifications to the SDK and maintains full type safety.
class MyDomainB1Client(AsyncB1Client):
    @property
    def return_requests(self) -> AsyncGenericResource[Document]:
        """Custom alias returning Document types from the ReturnRequests endpoint."""
        return self.get_resource(model=Document, endpoint="ReturnRequests")

async def main():
    setup_logging()
    
    env = B1Environment.load()
    config = env.config
    
    print(f"✅ Conectando a {config.base_url} (DB: {config.company_db})...")
    
    async with AsyncB1Client(config) as b1:
        
        print("\n============================================================")
        print("  1. THIN ALIASES (FIRST-CLASS CITIZENS)")
        print("============================================================")
        print("💡 The SDK provides 16 explicit properties (e.g. b1.items, b1.invoices) with full IDE typings.")
        
        # Example 1: Using the explicit `.items` thin alias
        try:
            # We catch exception just in case A0001 doesn't exist
            item: Item = await b1.items.get("A0001")
            print(f"✨ Item found via explicit property: {item.item_name} ({item.item_code})")
        except Exception as e:
            print(f"⚠️ Could not fetch Item A0001: {e}")

        
        print("\n============================================================")
        print("  2. DYNAMIC RESOURCES (GET_RESOURCE)")
        print("============================================================")
        print("💡 For any endpoint not in the Top 16, use `get_resource` to map a Pydantic Model to an endpoint.")
        
        # Example 2: Dynamically accessing the 'Quotations' endpoint.
        quotations_resource = b1.get_resource(model=Document, endpoint="Quotations")
        
        try:
            quotation = await quotations_resource.get(1)
            print(f"✨ Quotation found via dynamic resource: DocEntry {quotation.doc_entry}, Total: {quotation.doc_total}")
        except Exception as e:
            print(f"⚠️ Could not fetch Quotation 1: {e}")

    # Example 3: Using the Domain-Specific Subclass
    print("\n============================================================")
    print("  3. CUSTOM CLIENT SUBCLASSING")
    print("============================================================")
    print("💡 Subclassing is the best practice for Domain-Driven architectures.")
    
    async with MyDomainB1Client(config) as custom_client:
        try:
            return_request = await custom_client.return_requests.get(1)
            print(f"✨ Return Request found via subclass alias: DocEntry {return_request.doc_entry}")
        except Exception as e:
            print(f"⚠️ Could not fetch Return Request 1: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
