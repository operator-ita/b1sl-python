"""
Example 19: OData $batch requests (Generic & Environment-Agnostic)

Demonstrates how to group multiple SAP Service Layer operations into a single
HTTP request using environment-safe queries (top=1).

Covers:
    - Generic GET operations using fluent builders.
    - Transactional ChangeSets (Atomic operations).
    - Intelligent results container (BatchResults).
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

from b1sl.b1sl import AsyncB1Client, B1Environment
from b1sl.b1sl import entities as en


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

    # Random IDs for this run
    item_code_1 = f"BATCH_I1_{uuid.uuid4().hex[:4].upper()}"
    item_code_2 = f"BATCH_I2_{uuid.uuid4().hex[:4].upper()}"

    async with AsyncB1Client(env.config) as b1:

        # ── 2. Batch Execution: Generic Queries & Creating ────────────────────
        section("2. Batch Execution: Generic Queries & Create")
        
        print(f"Queuing operations for {item_code_1} and {item_code_2}...")
        
        async with b1.batch() as batch:
            # A. Generic Queries (env-agnostic using .top(1))
            await batch.items.top(1).execute()
            await batch.business_partners.top(1).execute()

            # B. Atomic ChangeSet
            async with batch.changeset() as cs:
                await cs.items.create(en.Item(
                    item_code=item_code_1,
                    item_name="Batch Generic Item 1"
                ))
                await cs.items.create(en.Item(
                    item_code=item_code_2,
                    item_name="Batch Generic Item 2"
                ))

            # EXPLICIT EXECUTION (Inside the block)
            # This is the canonical way: execute while the context is active.
            print("\nExecuting $batch request...")
            results = await batch.execute()

        # ── 3. Inspecting Results (Defensive Analysis Pattern) ────────────────
        section("3. Results Analysis")
        
        # NOTE: batch.execute() does NOT raise exceptions on failure.
        # This allows you to handle "Partial Success" (some operations OK, some failed).
        # We use a "Defensive Analysis" pattern:
        #   1. Check 'all_ok' for a fast boolean switch.
        #   2. Use 'r.index' for precise traceability of failures.
        #   3. Remember: ChangeSets are Atomic (All-or-Nothing).
        
        print(f"Total operations in batch: {len(results)}")
        print(f"Execution status: {'SUCCESS' if results.all_ok else 'PARTIAL FAILURE'}")
        
        # Access results by index (preserves enqueue order)
        if len(results) >= 2:
            if results[0].ok:
                items = results[0].entity
                print(f"✅ Op 0 (Items): Found {len(items)} item(s).")
            else:
                # Trace exactly why Op 0 failed
                print(f"❌ Op 0 failed: {results[0].error}")
            
            if results[1].ok:
                bps = results[1].entity
                print(f"✅ Op 1 (BP): Found {len(bps)} partner(s).")

        if results.all_ok:
            # Results 2 and 3 are the changeset creates (Atomic)
            print(f"✅ New Item 1 Created: {results[2].entity.item_code}")
            print(f"✅ New Item 2 Created: {results[3].entity.item_code}")
        else:
            # TRACEABILITY: Iterating over failed list only
            print("\nFailures detected:")
            for r in results.failed:
                print(f"  ❌ Operation {r.index} (Status {r.status}): {r.error}")

if __name__ == "__main__":
    asyncio.run(main())
