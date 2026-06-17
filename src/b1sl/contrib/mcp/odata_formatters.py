"""
b1sl.contrib.mcp.odata_formatters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MCP response formatters for SAP B1 OData entity results and exceptions.

All functions return plain strings (MCP TextContent value).
No MCP SDK dependency — wrap the output in whatever content type your server uses.

Typical usage::

    from b1sl.contrib.mcp.odata_formatters import format_entity, format_odata_error

    item = client.items.get("A001")
    text = format_entity(item, title="Item A001")

    try:
        client.orders.patch(1, en.Document(card_code="NEW"))
    except SAPConcurrencyError as e:
        msg = format_odata_error(e, resource="orders", key=1)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

    from b1sl.b1sl.models.base import B1Model


# ── Internal helpers ──────────────────────────────────────────────────────────

def _fmt_cell(value: object) -> str:
    """Escape and stringify a scalar value for a markdown table cell."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).replace("|", "\\|").replace("\n", " ")


def _sap_error_message(details: dict | None) -> str | None:
    """Extract the human-readable message from a SAP error response body."""
    if not isinstance(details, dict):
        return None
    try:
        return details["error"]["message"]["value"]
    except (KeyError, TypeError):
        pass
    # Fallback: some SAP versions use a flat "message" string
    try:
        msg = details["error"]["message"]
        if isinstance(msg, str):
            return msg
    except (KeyError, TypeError):
        pass
    return None


# ── Public formatters ─────────────────────────────────────────────────────────

def format_entity(
    model: "B1Model",
    *,
    title: str | None = None,
) -> str:
    """Format a B1Model instance as a markdown key/value table for LLM context.

    Boolean fields are already coerced to Python ``bool`` by the model;
    they render as ``true`` / ``false``.  Navigation properties (document lines,
    addresses) show a row count rather than the raw list.

    UDF fields (``U_`` prefix) appear under a separate *User-Defined Fields*
    section.  Both declared UDFs (in ``model_fields``) and runtime UDFs captured
    via Pydantic ``extra='allow'`` are rendered.

    Args:
        model: A hydrated B1Model instance (e.g. from ``client.items.get()``).
        title: Optional H2 heading inserted before the table.

    Returns:
        Markdown-formatted string ready for MCP ``TextContent``.

    Example::

        item = client.items.get("A001")
        text = format_entity(item, title="Item A001")
        # → "## Item A001\\n| Field | Value |\\n..."
    """
    lines: list[str] = []

    if title:
        lines.append(f"## {title}\n")

    # Merge declared fields (by SAP alias) with runtime extra fields (UDFs)
    data: dict = model.model_dump(by_alias=True)
    extra: dict = model.model_extra or {}
    data.update(extra)

    regular: list[tuple[str, object]] = []
    navigation: list[tuple[str, object]] = []
    udfs: list[tuple[str, object]] = []

    for key, value in data.items():
        if key == "@odata.etag":
            continue
        if isinstance(value, (list, dict)):
            navigation.append((key, value))
        elif key.startswith("U_"):
            udfs.append((key, value))
        else:
            regular.append((key, value))

    if not regular and not navigation and not udfs:
        lines.append("*No fields to display.*")
        return "\n".join(lines)

    lines.append("| Field | Value |")
    lines.append("| --- | --- |")
    for key, value in regular:
        lines.append(f"| {key} | {_fmt_cell(value)} |")
    for key, value in navigation:
        if isinstance(value, list):
            lines.append(f"| {key} | [{len(value)} items] |")
        else:
            lines.append(f"| {key} | [object] |")

    if udfs:
        lines.append("\n### User-Defined Fields\n")
        lines.append("| Field | Value |")
        lines.append("| --- | --- |")
        for key, value in udfs:
            lines.append(f"| {key} | {_fmt_cell(value)} |")

    return "\n".join(lines)


def format_collection(
    models: "Sequence[B1Model]",
    *,
    max_rows: int = 50,
    title: str | None = None,
    has_more: bool = False,
    total_count: int | None = None,
    next_skip: int | None = None,
) -> str:
    """Format a sequence of B1Model instances as a markdown table for LLM context.

    Derives column headers from the first model's scalar (non-navigation) fields.
    Navigation properties (``list`` / ``dict`` values) are excluded from the
    table — use ``format_entity`` for detailed single-entity views.

    Truncated rows are noted at the bottom.  Pass ``has_more=True`` when the
    OData response included an ``@odata.nextLink`` to hint the agent that further
    pages are available.

    Args:
        models: Hydrated B1Model instances — a plain list or the
            ``PaginatedResult`` returned by ``.list()`` / ``.execute()``.
        max_rows: Maximum rows to include in the table.  Rows beyond this are
            summarized as a footnote rather than omitted silently.
        title: Optional H2 heading inserted before the table.
        has_more: ``True`` when more rows exist beyond this page
            (``page.has_more``).
        total_count: Full result-set size (``page.total_count`` /
            ``@odata.count``), surfaced as a footnote when provided. ``None``
            unless the query opted in with ``$count=true``.
        next_skip: Absolute ``$skip`` for the next page (``page.next_skip``);
            when set, the continuation hint tells the agent to pass ``skip=N``.

    Returns:
        Markdown-formatted string ready for MCP ``TextContent``.

    Example::

        page = client.orders.execute()
        text = format_collection(
            page, title="Open Orders", has_more=page.has_more,
            total_count=page.total_count, next_skip=page.next_skip,
        )
        # → "## Open Orders\\n| DocEntry | CardCode | ...\\n..."
    """
    lines: list[str] = []

    if title:
        lines.append(f"## {title}\n")

    rows_to_show = models[:max_rows]
    truncated = len(models) - len(rows_to_show)

    if not rows_to_show:
        lines.append("*No records returned.*")
        return "\n".join(lines)

    # Derive scalar headers from the first model (exclude navigation + etag)
    first_data: dict = rows_to_show[0].model_dump(by_alias=True)
    first_extra: dict = rows_to_show[0].model_extra or {}
    first_data.update(first_extra)
    headers = [
        k for k, v in first_data.items()
        if k != "@odata.etag" and not isinstance(v, (list, dict))
    ]

    if not headers:
        lines.append("*No scalar fields to display.*")
        return "\n".join(lines)

    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")

    for model in rows_to_show:
        row_data: dict = model.model_dump(by_alias=True)
        row_extra: dict = model.model_extra or {}
        row_data.update(row_extra)
        cells = [_fmt_cell(row_data.get(h)) for h in headers]
        lines.append("| " + " | ".join(cells) + " |")

    footnotes: list[str] = []
    if truncated:
        footnotes.append(f"*{truncated} record(s) omitted (max_rows={max_rows})*")
    if total_count is not None:
        footnotes.append(f"*Total matching rows: {total_count}.*")
    if has_more:
        nxt = f"pass `skip={next_skip}` for the next page, or " if next_skip is not None else ""
        footnotes.append(
            f"*More rows available — {nxt}use `page_size`/`max_pages` to stream further.*"
        )
    if footnotes:
        lines.append("\n" + "  ".join(footnotes))

    return "\n".join(lines)


def format_odata_error(
    exc: Exception,
    *,
    resource: str | None = None,
    key: object = None,
) -> str:
    """Format a b1sl OData exception as a diagnostic message for LLMs.

    Provides actionable hints based on the exception type so the agent can
    self-correct without requiring a human to read the raw SAP error body.

    Args:
        exc: The caught exception — any ``B1Exception`` subclass.
        resource: Elite alias of the resource being accessed (adds context).
        key: Primary key value attempted (adds context for 404/412 messages).

    Returns:
        Plain text error message suitable for MCP error content or tool output.

    Example::

        try:
            client.orders.patch(99, en.Document(card_code="NEW"))
        except SAPConcurrencyError as e:
            msg = format_odata_error(e, resource="orders", key=99)
            # → "Concurrency conflict on orders(99): ETag stale..."
    """
    from b1sl.b1sl.exceptions.exceptions import (
        B1AuthError,
        B1ConnectionError,
        B1NotFoundError,
        B1ValidationError,
        SAPConcurrencyError,
    )

    ctx_parts: list[str] = []
    if resource:
        ctx_parts.append(resource)
        if key is not None:
            ctx_parts.append(f"({key})")
    ctx = " ".join(ctx_parts)
    ctx_prefix = f" on {ctx}" if ctx else ""

    if isinstance(exc, SAPConcurrencyError):
        endpoint_hint = f" on {exc.endpoint}" if exc.endpoint else ""
        return (
            f"Concurrency conflict{ctx_prefix or endpoint_hint}: "
            "the ETag no longer matches the current server state (HTTP 412). "
            "Another process modified this record since your last GET. "
            "Recovery: re-fetch the entity with a GET to obtain a fresh ETag, "
            "then re-apply your changes and retry the PATCH. "
            "This is optimistic locking — not a permanent failure."
        )

    if isinstance(exc, B1NotFoundError):
        key_hint = f" with key {key!r}" if key is not None else ""
        resource_hint = f" in {resource!r}" if resource else ""
        return (
            f"Record not found{key_hint}{resource_hint} (HTTP 404). "
            "Verify the primary key is correct and the record exists in SAP. "
            f"SAP message: {exc}"
        )

    if isinstance(exc, B1AuthError):
        return (
            f"Authentication error{ctx_prefix} (HTTP 401): "
            "the SAP session has expired or the credentials are invalid. "
            "Reconnect the client (call login() or recreate the client) before retrying. "
            f"SAP message: {exc}"
        )

    if isinstance(exc, B1ValidationError):
        sap_msg = _sap_error_message(getattr(exc, "details", None))
        sap_hint = f"\nSAP field-level detail: {sap_msg}" if sap_msg else f"\nSAP message: {exc}"
        return (
            f"Validation error{ctx_prefix} (HTTP 400): "
            "SAP rejected the payload — check required fields, value ranges, "
            "and business-rule constraints. "
            "Ensure boolean fields use Python bool (true/false), not 'tYES'/'tNO', "
            "in PATCH/CREATE payloads."
            + sap_hint
        )

    if isinstance(exc, B1ConnectionError):
        return (
            f"Connection error{ctx_prefix}: could not reach the SAP Service Layer. "
            "Check network connectivity, the server URL, and that the SAP B1 service is running. "
            f"Detail: {exc}"
        )

    return f"SAP B1 error{ctx_prefix}: {exc}"
