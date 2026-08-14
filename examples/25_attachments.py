"""
Example 25: Attachments — Multipart Upload and Binary Download (Attachments2)

Demonstrates ``client.attachments`` and the generic non-JSON primitives:
- Uploading a single file with ``upload()``.
- Uploading several files in one request (one entry, several lines).
- Uploading straight from disk via ``MultipartFile.from_path()``.
- Downloading a file's raw bytes with ``download()``.
- Reading attachment metadata through ordinary typed CRUD.
- Linking an attachment to a document via ``AttachmentEntry``.
- The generic escape hatches ``post_multipart()`` / ``get_binary()``.
- Dry-run interception of an upload.
- Async client parity with ``AsyncB1Client``.

Two SAP behaviours worth knowing (see ``docs/18-sap-version-quirks.md`` Q4):
- The upload body is files-only with the fixed field name ``files``. The
  two-part JSON+binary shape from SAP's manual §3.17.3 is rejected (400 -1000).
- ``DELETE Attachments2(N)`` is not implemented by SAP in any version.

Prerequisites:
    B1SL_BASE_URL, B1SL_USERNAME, B1SL_PASSWORD, B1SL_COMPANY_DB env vars
    (or a populated .env file at the project root).

    The Service Layer's attachments folder must be reachable server-side;
    otherwise SAP answers 404 "Fail to get the LINUX mount point for
    AttachmentsFolderPath" — an infrastructure issue, not an SDK one.
"""
import asyncio
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from b1sl.b1sl import AsyncB1Client, B1Client, B1Environment, MultipartFile
from b1sl.b1sl.exceptions.exceptions import B1Exception, B1NotFoundError

# ── Helpers ───────────────────────────────────────────────────────────────────

SAMPLE_TXT = b"b1sl attachment demo\n"
SAMPLE_PDF = b"%PDF-1.4\n% b1sl demo\ntrailer\n%%EOF\n"


def section(title: str) -> None:
    print(f"\n{'─' * 70}")
    print(f"  {title}")
    print(f"{'─' * 70}")


# ── Scenario 1: upload one file ───────────────────────────────────────────────

def demo_upload_single(client: B1Client) -> int:
    """Upload one file and return the new AbsoluteEntry."""
    section("1. Upload a single file")

    entry = client.attachments.upload(MultipartFile("notes.txt", SAMPLE_TXT))

    print(f"  AbsoluteEntry: {entry.absolute_entry}")
    for line in entry.attachments2_lines or []:
        print(f"    line {line.line_num}: {line.file_name}.{line.file_extension}")
    return entry.absolute_entry


# ── Scenario 2: several files in one request ──────────────────────────────────

def demo_upload_multiple(client: B1Client) -> int:
    """One POST -> one entry holding one line per file."""
    section("2. Upload several files in one request")

    entry = client.attachments.upload([
        MultipartFile("contract.txt", SAMPLE_TXT),
        MultipartFile("annex.pdf", SAMPLE_PDF),
    ])

    print(f"  AbsoluteEntry: {entry.absolute_entry}")
    print(f"  lines created: {len(entry.attachments2_lines or [])}")
    return entry.absolute_entry


# ── Scenario 3: upload from disk ──────────────────────────────────────────────

def demo_upload_from_path(client: B1Client) -> int:
    """MultipartFile.from_path() reads the bytes and reuses the file's name."""
    section("3. Upload straight from disk")

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "from_disk.txt"
        path.write_bytes(SAMPLE_TXT)

        entry = client.attachments.upload(MultipartFile.from_path(path))

    print(f"  AbsoluteEntry: {entry.absolute_entry}")
    return entry.absolute_entry


# ── Scenario 4: download ──────────────────────────────────────────────────────

def demo_download(client: B1Client, entry_id: int) -> None:
    """Fetch a file's raw bytes back."""
    section("4. Download a file")

    blob = client.attachments.download(entry_id, "notes.txt")
    print(f"  bytes received: {len(blob)}")
    print(f"  round-trip intact: {blob == SAMPLE_TXT}")

    # SAP stores the name and extension apart; passing them separately works too.
    same = client.attachments.download(entry_id, "notes", "txt")
    print(f"  split name/extension gives the same bytes: {same == blob}")

    # A missing file (deleted outside SAP) surfaces as 404 -2028.
    try:
        client.attachments.download(entry_id, "does_not_exist.txt")
    except B1NotFoundError as e:
        print(f"  missing file -> B1NotFoundError: {str(e)[:60]}...")


# ── Scenario 5: metadata via ordinary typed CRUD ──────────────────────────────

def demo_metadata(client: B1Client, entry_id: int) -> None:
    """Metadata is plain JSON — the inherited GenericResource methods apply."""
    section("5. Read attachment metadata")

    meta = client.attachments.get(entry_id)
    for line in meta.attachments2_lines or []:
        print(
            f"  line {line.line_num}: {line.file_name}.{line.file_extension} "
            f"(path: {line.source_path})"
        )


# ── Scenario 6: link an attachment to a document ──────────────────────────────

def demo_link_to_document(client: B1Client, entry_id: int) -> None:
    """AbsoluteEntry is what a document's AttachmentEntry field points at."""
    section("6. Link an attachment to a document")

    print("  Documents reference an attachment by AbsoluteEntry:")
    print(f"    client.orders.update(123, en.Document(attachment_entry={entry_id}))")
    print("  (not executed here — it would modify a real order)")


# ── Scenario 7: generic primitives ────────────────────────────────────────────

def demo_generic_primitives(client: B1Client) -> None:
    """post_multipart/get_binary work against any endpoint needing a raw body."""
    section("7. Generic primitives (any endpoint)")

    data = client.post_multipart(
        "Attachments2", MultipartFile("generic.txt", SAMPLE_TXT)
    )
    entry_id = data["AbsoluteEntry"]
    print(f"  post_multipart -> AbsoluteEntry {entry_id}")

    blob = client.get_binary(
        f"Attachments2({entry_id})/$value", {"filename": "'generic.txt'"}
    )
    print(f"  get_binary -> {len(blob)} bytes")


# ── Scenario 8: dry-run ───────────────────────────────────────────────────────

def demo_dry_run(client: B1Client) -> None:
    """Uploads are writes, so dry-run intercepts them like any other write."""
    section("8. Dry-run interception")

    with client.dry_run():
        entry = client.attachments.upload(MultipartFile("never_sent.txt", b"x"))

    print(f"  nothing sent; synthesized entry: {entry.absolute_entry!r}")


# ── Scenario 9: what SAP does not support ─────────────────────────────────────

def demo_unsupported_delete(client: B1Client, entry_id: int) -> None:
    """SAP never implemented DELETE for Attachments2 — in any version."""
    section("9. DELETE is unsupported server-side")

    try:
        client.attachments.delete(entry_id)
        print("  unexpected: SAP accepted the delete")
    except B1Exception as e:
        print(f"  expected failure -> {str(e)[:70]}...")
    print("  Remove the line via update() on Attachments2_Lines instead.")


# ── Scenario 10: async parity ─────────────────────────────────────────────────

async def demo_async(env: B1Environment) -> None:
    section("10. Async parity")

    async with AsyncB1Client(env.config) as b1:
        entry = await b1.attachments.upload(
            MultipartFile("async_notes.txt", SAMPLE_TXT)
        )
        print(f"  uploaded AbsoluteEntry: {entry.absolute_entry}")

        blob = await b1.attachments.download(
            entry.absolute_entry, "async_notes.txt"
        )
        print(f"  downloaded {len(blob)} bytes; intact: {blob == SAMPLE_TXT}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    env = B1Environment.load()

    with B1Client(env.config) as client:
        entry_id = demo_upload_single(client)
        demo_upload_multiple(client)
        demo_upload_from_path(client)
        demo_download(client, entry_id)
        demo_metadata(client, entry_id)
        demo_link_to_document(client, entry_id)
        demo_generic_primitives(client)
        demo_dry_run(client)
        demo_unsupported_delete(client, entry_id)

    asyncio.run(demo_async(env))

    print(f"\n{'═' * 70}")
    print("  All attachment scenarios completed.")
    print(f"{'═' * 70}\n")


if __name__ == "__main__":
    main()
