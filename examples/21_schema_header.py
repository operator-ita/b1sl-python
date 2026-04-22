"""
Example 21: B1S-Schema Header Support (Generic & Environment-Agnostic)

Demonstrates how to use the `B1S-Schema` header to restrict field payloads
returned by SAP Service Layer.

Key Concepts:
    - Reduced payload size and improved performance.
    - Context-isolated schema application using `ContextVar`.
    - Fluent API and Scoped Context Manager patterns.
"""
import asyncio
import sys
from pathlib import Path

# ── Path hack ────────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from b1sl.b1sl import AsyncB1Client, B1Environment
from b1sl.b1sl import exceptions as ex


# ─────────────────────────────────────────────────────────────────────────────
# Helper: pretty-print a section header
# ─────────────────────────────────────────────────────────────────────────────
def section(title: str) -> None:
    print(f"\n{'─' * 80}")
    print(f"  {title}")
    print(f"{'─' * 80}")

async def main() -> None:
    section("1. Setup Environment")
    try:
        env = B1Environment.load(strict=True)
        print("✅ Environment loaded.")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return

    async with AsyncB1Client(env.config) as b1:

        # ── 2. Fluent API Usage ───────────────────────────────────────────────
        section("2. Fluent API: Applying a Schema to a Specific Request")
        
        print("Executing request with 'demo.schema'...")
        # Note: 'demo.schema' must exist on the SAP server's conf directory.
        try:
            items = await b1.items.with_schema("demo.schema").top(1).execute()
            print(f"✅ Success! Received {len(items)} item(s) using demo.schema.")
        except ex.B1Exception as e:
            print(f"❌ Schema error: {e}")

        # ── 3. Scoped Context Manager ─────────────────────────────────────────
        section("3. Scoped Context Manager: Applying a Schema to a Block")
        
        # This is the most Pythonic way to apply a schema to multiple operations
        # while ensuring thread/task isolation.
        print("Entering scoped block with 'demo.schema'...")
        with b1.with_schema("demo.schema"):
            try:
                item = await b1.items.top(1).execute()
                bp = await b1.business_partners.top(1).execute()
                print("✅ Success! Both operations used demo.schema.")
                print(f"   - Item Code: {item[0].item_code if item else 'N/A'}")
                print(f"   - BP CardCode: {bp[0].card_code if bp else 'N/A'}")
            except ex.B1Exception as e:
                print(f"❌ Block error: {e}")

        # ── 4. Error Handling: Invalid Schema ─────────────────────────────────
        section("4. Error Handling: What happens if the schema is missing?")
        
        print("Attempting to use a non-existent schema 'missing.schema'...")
        try:
            # SAP will return a 500 Internal Server Error if the file is not found
            await b1.items.with_schema("missing.schema").top(1).execute()
        except ex.B1Exception as e:
            print("✅ Correctly caught the expected SAP error:")
            print(f"   {e}")

if __name__ == "__main__":
    asyncio.run(main())
