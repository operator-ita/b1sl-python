"""
examples/etag_concurrency.py
============================
Demonstrates ETag-based Optimistic Concurrency Control (OCC) in the SAP B1 SDK.

Covers:
  1. Automatic ETag extraction from a GET response (header-first, body fallback).
  2. Automatic If-Match injection on a subsequent PATCH / OData Action.
  3. Handling SAPConcurrencyError (HTTP 412 / code -2039) in a Temporal.io-style
     retry loop.
  4. Sync adapter mirror for completeness.

Run from the repository root:
    uv run python examples/etag_concurrency.py
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

# ── Path hack so the example runs from the repo root without installing ──────
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from b1sl.b1sl import AsyncRestAdapter, SAPConcurrencyError
from examples.utils import build_async_client  # type: ignore[import]

# ════════════════════════════════════════════════════════════════════════════
#  1. Basic ETag flow  (GET → automatic cache → PATCH with If-Match)
# ════════════════════════════════════════════════════════════════════════════

async def update_business_partner_phone(
    adapter: AsyncRestAdapter,
    card_code: str,
    new_phone: str,
) -> None:
    """
    Fetches a BusinessPartner (caching its ETag) then PATCHes only the Phone1
    field.  If a concurrent modification occurred between the GET and the PATCH,
    SAP returns 412 and the SDK raises SAPConcurrencyError.

    Args:
        adapter:   An *already-authenticated* AsyncRestAdapter instance.
        card_code: The BusinessPartner CardCode (e.g. ``"C20000"``).
        new_phone: The new phone number to write.
    """
    endpoint = f"/BusinessPartners('{card_code}')"

    # ── Step 1: GET — ETag is extracted automatically from the response header
    #            (falls back to @odata.etag in the body if the header is absent)
    result = await adapter.get(endpoint)
    bp = result.data
    print(f"[GET]   {card_code} → Phone1={bp.get('Phone1')!r}")

    # Peek at what was cached (for illustration only — you never need to do this)
    cached_etag = adapter._etag_cache.get(endpoint)
    print(f"[CACHE] ETag stored: {cached_etag!r}")

    # ── Step 2: PATCH — If-Match is injected automatically from the cache.
    #            If no ETag was cached SAP performs a blind override (by design).
    payload = {"Phone1": new_phone}
    await adapter.patch(endpoint, data=payload)
    print(f"[PATCH] {card_code} Phone1 updated to {new_phone!r}")


# ════════════════════════════════════════════════════════════════════════════
#  2. OData Actions  (e.g. /BusinessPartners('C20000')/Cancel)
#     POST actions also receive If-Match because the cache key is the *resource*
#     endpoint, and _build_headers covers POST in PATCH/DELETE/POST set.
# ════════════════════════════════════════════════════════════════════════════

async def cancel_order(
    adapter: AsyncRestAdapter,
    doc_entry: int,
) -> None:
    """Cancel a Sales Order using an OData Action (HTTP POST).

    The SDK injects If-Match automatically if the order was previously
    fetched via GET and its ETag is cached.

    Args:
        adapter:   An *already-authenticated* AsyncRestAdapter instance.
        doc_entry: The DocEntry of the Sales Order to cancel.
    """
    resource_endpoint = f"/Orders({doc_entry})"
    action_endpoint   = f"/Orders({doc_entry})/Cancel"

    # Warm up the ETag cache with a GET
    await adapter.get(resource_endpoint)
    cached_etag = adapter._etag_cache.get(resource_endpoint)
    print(f"[GET]   Order {doc_entry} — ETag cached: {cached_etag!r}")

    # The Action endpoint (POST) shares the SAME If-Match value as the resource
    # because _build_headers looks up the *base* resource key.
    # NOTE: if SAP uses the exact action URL as the ETag key you would call
    #       _build_headers with resource_endpoint explicitly; adjust per your
    #       server's behaviour.
    await adapter.post(action_endpoint)
    print(f"[POST]  /Orders({doc_entry})/Cancel — action executed with If-Match")


# ════════════════════════════════════════════════════════════════════════════
#  3. Temporal.io-style retry loop for SAPConcurrencyError
# ════════════════════════════════════════════════════════════════════════════

MAX_CONCURRENCY_RETRIES = 3


async def robust_update_phone(
    adapter: AsyncRestAdapter,
    card_code: str,
    new_phone: str,
) -> None:
    """
    Retries the GET → PATCH cycle up to MAX_CONCURRENCY_RETRIES times when
    a SAPConcurrencyError (HTTP 412 / -2039) is detected.

    In a real Temporal.io Activity you would simply let SAPConcurrencyError
    propagate — Temporal's retry policy handles restarts automatically.
    This loop demonstrates the *manual* equivalent for non-Temporal contexts.

    Args:
        adapter:   An *already-authenticated* AsyncRestAdapter instance.
        card_code: The BusinessPartner CardCode.
        new_phone: The new phone number to write.
    """
    endpoint = f"/BusinessPartners('{card_code}')"

    for attempt in range(1, MAX_CONCURRENCY_RETRIES + 1):
        try:
            result = await adapter.get(endpoint)
            print(f"[Attempt {attempt}] ETag: {adapter._etag_cache.get(endpoint)!r}")

            await adapter.patch(endpoint, data={"Phone1": new_phone})
            print(f"[Attempt {attempt}] PATCH succeeded ✓")
            return  # success — exit the retry loop

        except SAPConcurrencyError as exc:
            print(
                f"[Attempt {attempt}] 412 Conflict detected — "
                f"ETag sent: {exc.etag_sent!r}, SAP code: {exc.sap_code}"
            )
            if attempt == MAX_CONCURRENCY_RETRIES:
                print("Max retries reached. Giving up.")
                raise  # re-raise for the caller / Temporal to handle
            print("Retrying with fresh GET …\n")

    # Unreachable, but keeps type checkers happy
    raise RuntimeError("Exhausted retry loop without succeeding or raising")  # noqa: EM101


# ════════════════════════════════════════════════════════════════════════════
#  4. Temporal.io Activity skeleton  (not executed — documentation only)
# ════════════════════════════════════════════════════════════════════════════

TEMPORAL_EXAMPLE = '''
# In a real Temporal.io Worker you would write:

from temporalio import activity
from temporalio.exceptions import ApplicationError
from b1sl.b1sl import AsyncRestAdapter, SAPConcurrencyError

@activity.defn
async def update_bp_phone_activity(card_code: str, new_phone: str) -> None:
    """
    Temporal Activity.  SAPConcurrencyError is declared retryable so Temporal
    will restart the activity automatically (which re-fetches the resource and
    retrieves a fresh ETag before retrying the PATCH).
    """
    async with AsyncRestAdapter.from_config(config) as adapter:
        endpoint = f"/BusinessPartners(\'{card_code}\')"
        try:
            await adapter.get(endpoint)         # caches ETag
            await adapter.patch(endpoint, data={"Phone1": new_phone})
        except SAPConcurrencyError as e:
            # non_retryable=False → Temporal will retry according to its policy
            raise ApplicationError(str(e), non_retryable=False) from e
'''


# ════════════════════════════════════════════════════════════════════════════
#  Entry point
# ════════════════════════════════════════════════════════════════════════════

async def main() -> None:
    print("=" * 60)
    print("SAP B1 SDK — ETag Optimistic Concurrency Control Demo")
    print("=" * 60)
    print()

    try:
        config = build_async_client()  # loads .env / config.json
    except Exception as e:
        print(f"[SKIP] Could not load SAP credentials: {e}")
        print("       This example requires a live SAP B1 Service Layer.")
        print()
        print("Temporal.io Activity skeleton:")
        print(TEMPORAL_EXAMPLE)
        return

    async with AsyncRestAdapter.from_config(config) as adapter:
        card_code = "C20000"        # adjust to a valid CardCode in your system
        new_phone = "+1-555-0199"

        print("── 1. Basic GET → PATCH flow ─────────────────────────────")
        try:
            await update_business_partner_phone(adapter, card_code, new_phone)
        except SAPConcurrencyError as exc:
            print(f"  [412] Concurrency conflict: {exc} (etag_sent={exc.etag_sent!r})")
        except Exception as exc:
            print(f"  [ERR] {exc}")

        print()
        print("── 3. Robust retry loop ──────────────────────────────────")
        try:
            await robust_update_phone(adapter, card_code, new_phone)
        except SAPConcurrencyError:
            print("  All retries exhausted — manual intervention required.")
        except Exception as exc:
            print(f"  [ERR] {exc}")

    print()
    print("── Temporal.io Activity skeleton ─────────────────────────")
    print(TEMPORAL_EXAMPLE)


if __name__ == "__main__":
    asyncio.run(main())
