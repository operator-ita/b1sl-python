from urllib.parse import parse_qs, urlparse

from b1sl.b1sl.exceptions.exceptions import B1PaginationError


def extract_next_link(data: dict) -> str | None:
    """Return the OData nextLink from a response body, tolerating v3 and v4 formats.

    SAP Service Layer uses different key names depending on the OData version:
    - OData v3 (``b1s/v1``): ``"odata.nextLink"``
    - OData v4 (``b1s/v2``): ``"@odata.nextLink"``

    Returns the first non-empty value found, or ``None``.
    """
    return data.get("@odata.nextLink") or data.get("odata.nextLink") or None


def extract_odata_count(data: dict) -> int | None:
    """Return the OData inline total count from a response body, or ``None``.

    Present only when the request asked for it via ``$count=true``. Tolerates
    both OData formats: ``"@odata.count"`` (v4) and ``"odata.count"`` (v3). It is
    the total number of entities matching the query, independent of paging.
    """
    raw = data.get("@odata.count")
    if raw is None:
        raw = data.get("odata.count")
    if raw is None:
        return None
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


def extract_skip(next_link: str) -> int | None:
    """
    Extracts the $skip value from an odata.nextLink string.
    
    Args:
        next_link: The raw odata.nextLink URL string returned by SAP.
        
    Returns:
        The integer value of $skip if found, else None.
    """
    parsed_url = urlparse(next_link)
    query_params = parse_qs(parsed_url.query)
    skip_val = query_params.get("$skip")
    if skip_val:
        try:
            return int(skip_val[0])
        except (ValueError, IndexError):
            return None
    return None


def prepare_top_probe(request_params: dict) -> tuple[dict, int | None, int]:
    """Rewrite a request that carries ``$top`` into a fence-post probe.

    SAP B1 Service Layer omits ``@odata.nextLink`` when the requested ``$top``
    is satisfied within a single server page (``top <= effective page size``) —
    from its perspective the request is "done", so ``has_more`` derived from the
    nextLink reads ``False`` even when more matching rows exist (silent
    truncation). This is the common case: a small ``.top(20)`` on a large
    collection. (When ``top`` spans multiple server pages SAP does return a
    nextLink, but ``has_more`` must still be correct, and this probe handles
    both regimes uniformly.)

    To detect a further page without a separate ``$count`` round-trip, we ask
    SAP for one extra row (``$top + 1``) and let the caller truncate back to the
    requested ``$top``. If the extra row materialises, more rows exist.

    Returns a ``(probe_params, top, base_skip)`` tuple:

    - ``probe_params``: a *copy* of ``request_params`` with ``$top`` bumped by
      one (or the original dict unchanged when no positive ``$top`` is present).
    - ``top``: the caller's original ``$top`` as an int, or ``None`` when the
      fence-post does not apply (no ``$top``, non-integer, or ``$top <= 0``).
    - ``base_skip``: the caller's original ``$skip`` as an int (0 when absent),
      used to synthesise the next page's cursor.
    """
    top_raw = request_params.get("$top")
    if top_raw is None:
        return request_params, None, 0
    try:
        top = int(top_raw)
    except (TypeError, ValueError):
        return request_params, None, 0
    if top <= 0:
        # top=0 would loop forever on a synthesised, non-advancing cursor.
        return request_params, None, 0
    try:
        base_skip = int(request_params.get("$skip") or 0)
    except (TypeError, ValueError):
        base_skip = 0
    probe = dict(request_params)
    probe["$top"] = str(top + 1)
    return probe, top, base_skip


def build_next_params(current_params: dict, next_link: str) -> dict:
    """
    Builds the ep_params dictionary for the subsequent page request.
    
    Rule of Precedence (Defensive Implementation):
    1. 'next_link' ONLY wins for the $skip parameter.
    2. 'current_params' wins for everything else ($filter, $select, $orderby, etc.)
       Reason: SAP Service Layer inconsistently omits filters/selections in the 
       odata.nextLink URL. Re-applying current_params ensures the stream doesn't 
       silently "leak" outside its initial scope in page 2+.
    
    Args:
        current_params: The parameters used in the current (or initial) request.
        next_link: The raw odata.nextLink URL string returned by SAP.
        
    Returns:
        A new dictionary with combined parameters.
    """
    parsed_url = urlparse(next_link)
    next_query_params = parse_qs(parsed_url.query)

    # We start with a copy of current_params to preserve filters/selectors
    new_params = current_params.copy()

    # Take ONLY the cursor parameters from the next_link. SAP normally pages
    # with $skip; some endpoints/versions page with an opaque $skiptoken —
    # ignoring it would re-request the same page forever.
    next_skip = next_query_params.get("$skip")
    if next_skip:
        new_params["$skip"] = next_skip[0]
    next_skiptoken = next_query_params.get("$skiptoken")
    if next_skiptoken:
        new_params["$skiptoken"] = next_skiptoken[0]

    if not next_skip and not next_skiptoken:
        raise B1PaginationError(
            "odata.nextLink carries no recognised cursor ($skip/$skiptoken); "
            f"following it would loop on the same page. nextLink={next_link!r}"
        )

    return new_params
