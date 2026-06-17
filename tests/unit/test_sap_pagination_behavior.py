"""Regression tests that pin SAP B1 Service Layer's *observed* pagination and
boolean-filter behavior, so the fixes that depend on it can't silently regress.

The ``FakeServiceLayer`` below is a synthetic model of how a real SAP B1 10.0
server responds — derived from black-box probing, with NO connection details,
credentials, or customer data (everything here is generated). The two behaviors
it reproduces, and why they matter:

1. **Boolean fields are ``BoYesNoEnum`` (tYES/tNO), never ``Edm.Boolean``.**
   SAP rejects ``$filter=Frozen eq false`` with HTTP 400; only ``eq 'tNO'``
   works. (Guards the ``format_odata_value(bool)`` fix.)

2. **``@odata.nextLink`` is omitted when ``$top`` is satisfied within a single
   server page** (``top <= page size``). A small ``.top(N)`` on a large
   collection therefore returns no nextLink, so a naive ``has_more`` reads
   ``False`` even though more rows exist. When ``top`` spans multiple pages SAP
   *does* return a nextLink. (Guards the ``has_more`` fence-post and the
   ``.page_size()`` / stream behavior.)
"""
import re
from unittest.mock import AsyncMock, MagicMock

import pytest

from b1sl.b1sl.async_rest_adapter import AsyncRestAdapter
from b1sl.b1sl.exceptions.exceptions import B1ValidationError
from b1sl.b1sl.fields import Item
from b1sl.b1sl.models.base import B1Model
from b1sl.b1sl.models.paginated_result import PaginatedResult
from b1sl.b1sl.models.result import Result
from b1sl.b1sl.resources.async_base import AsyncGenericResource
from b1sl.b1sl.resources.base import GenericResource, ODataQuery
from b1sl.b1sl.rest_adapter import RestAdapter

# Synthetic, non-sensitive host used only to carry the $skip cursor.
_FAKE_NEXTLINK_HOST = "https://sl.test/b1s/v2/Items"
_SERVER_DEFAULT_PAGE = 20  # SAP's default B1S-PageSize
_FIELD_MAP = {"ItemCode": "item_code", "Frozen": "frozen"}


class MockModel(B1Model):
    item_code: str | None = None
    frozen: str | None = None


class FakeServiceLayer:
    """A deterministic, synthetic stand-in for SAP B1's ``Items`` collection."""

    def __init__(self, total: int = 100, frozen_count: int = 3) -> None:
        # The first `frozen_count` items are tYES, the rest tNO.
        self.items = [
            {"item_code": f"I{i:04d}", "frozen": "tYES" if i < frozen_count else "tNO"}
            for i in range(total)
        ]

    # ── filter evaluation (only what the tests exercise) ─────────────────────
    def _filtered(self, flt: str) -> list[dict]:
        if not flt:
            return self.items
        m = re.fullmatch(r"(\w+) eq '([^']*)'", flt)
        if not m:
            return self.items
        field, value = m.groups()
        key = _FIELD_MAP.get(field, field)
        return [it for it in self.items if str(it.get(key)) == value]

    # ── the server contract ──────────────────────────────────────────────────
    def serve(self, endpoint, ep_params=None, data=None, headers=None) -> Result:
        ep_params = ep_params or {}
        headers = headers or {}
        flt = ep_params.get("$filter", "")

        # SAP rejects bare boolean literals on BoYesNoEnum fields with HTTP 400.
        if re.search(r"\beq (true|false)\b", flt):
            raise B1ValidationError("Invalid value for BoYesNoEnum field (expected tYES/tNO)")

        rows = self._filtered(flt)

        if endpoint.endswith("/$count"):
            return Result(status_code=200, data=str(len(rows)))

        skip = int(ep_params.get("$skip", 0))
        top = ep_params.get("$top")
        top = int(top) if top is not None else None
        page = int(headers.get("B1S-PageSize", _SERVER_DEFAULT_PAGE))

        window = rows[skip:]
        if top is not None:
            # OData applies $top relative to this request's $skip.
            window = window[:top]
        returned = window[:page]

        # The crux: a nextLink is emitted ONLY when more rows remain within the
        # window — i.e. when $top did NOT fit inside this single page.
        has_next = len(window) > len(returned)
        next_link = f"{_FAKE_NEXTLINK_HOST}?$skip={skip + len(returned)}" if has_next else None

        # @odata.count: SAP returns the full filtered total (independent of paging)
        # only when the request opts in via $count=true. The adapter extracts it
        # into Result.total_count (verified live against a 10.0 HANA server).
        total_count = len(rows) if ep_params.get("$count") == "true" else None

        return Result(
            status_code=200,
            data={"value": returned},
            next_link=next_link,
            metadata="$metadata#Items",
            total_count=total_count,
        )


def _sync_resource(server: FakeServiceLayer) -> GenericResource[MockModel]:
    adapter = MagicMock(spec=RestAdapter)
    adapter.get.side_effect = server.serve
    res: GenericResource[MockModel] = GenericResource(adapter)
    res.endpoint = "Items"
    res.model = MockModel
    return res


def _async_resource(server: FakeServiceLayer) -> AsyncGenericResource[MockModel]:
    adapter = MagicMock(spec=AsyncRestAdapter)

    async def _aserve(endpoint, ep_params=None, data=None, headers=None):
        return server.serve(endpoint, ep_params=ep_params, data=data, headers=headers)

    adapter.get = AsyncMock(side_effect=_aserve)
    res: AsyncGenericResource[MockModel] = AsyncGenericResource(adapter)
    res.endpoint = "Items"
    res.model = MockModel
    return res


# ──────────────────────────────────────────────────────────────────────────────
# 1. Boolean filters — BoYesNoEnum (tYES/tNO), not Edm.Boolean
# ──────────────────────────────────────────────────────────────────────────────

def test_boolean_filter_uses_tyes_tno_and_is_accepted():
    res = _sync_resource(FakeServiceLayer())

    # The SDK renders the BoYesNoEnum literal...
    assert str(Item.frozen == False) == "Frozen eq 'tNO'"  # noqa: E712

    # ...and the server accepts it, returning only tNO rows.
    page = res.filter(Item.frozen == False).top(3).execute()  # noqa: E712
    assert isinstance(page, PaginatedResult)
    assert len(page) == 3
    assert all(item.frozen == "tNO" for item in page)


def test_legacy_boolean_literal_is_rejected_like_real_sap():
    res = _sync_resource(FakeServiceLayer())
    with pytest.raises(B1ValidationError):
        res.filter("Frozen eq false").top(1).execute()


# ──────────────────────────────────────────────────────────────────────────────
# 2. has_more fence-post — correct even when SAP omits the nextLink under $top
# ──────────────────────────────────────────────────────────────────────────────

def test_has_more_true_when_top_fits_one_page_but_more_rows_exist():
    # 100 rows; top=2 fits the 20-row server page, so SAP returns NO nextLink.
    res = _sync_resource(FakeServiceLayer(total=100))

    page = res.top(2).execute()

    assert isinstance(page, PaginatedResult)
    assert len(page) == 2
    # Without the fence-post this would be False (the live-server bug).
    assert page.has_more is True
    assert page.next_params is not None
    assert page.next_params["$skip"] == "2"


def test_has_more_false_on_genuine_single_page():
    # A unique-code filter returns exactly one row; top(5) over-asks.
    res = _sync_resource(FakeServiceLayer(total=100))

    page = res.filter(Item.item_code == "I0042").top(5).execute()

    assert isinstance(page, PaginatedResult)
    assert len(page) == 1
    assert page.has_more is False
    assert page.next_params is None


def test_has_more_walks_to_the_end_without_overrun():
    res = _sync_resource(FakeServiceLayer(total=5))

    seen: list[str] = []
    page = res.top(2).execute()
    assert isinstance(page, PaginatedResult)
    seen += [m.item_code for m in page]
    guard = 0
    while page.has_more and guard < 10:
        guard += 1
        page = res.list(params=page.next_params)
        seen += [m.item_code for m in page]

    assert seen == [f"I{i:04d}" for i in range(5)]
    assert page.has_more is False


# ──────────────────────────────────────────────────────────────────────────────
# 3. page_size — bounds the server page and yields a nextLink-driven has_more
# ──────────────────────────────────────────────────────────────────────────────

def test_page_size_bounds_page_and_reports_has_more():
    res = _sync_resource(FakeServiceLayer(total=100))

    page = res.page_size(3).execute()

    assert isinstance(page, PaginatedResult)
    assert len(page) == 3
    assert page.has_more is True
    assert res._adapter.get.call_args.kwargs["headers"] == {"B1S-PageSize": "3"}  # type: ignore[attr-defined]


# ──────────────────────────────────────────────────────────────────────────────
# 4. stream() + $top — crosses page boundaries, capped client-side, no truncation
# ──────────────────────────────────────────────────────────────────────────────

def test_stream_top_greater_than_page_size_yields_all_requested():
    res = _sync_resource(FakeServiceLayer(total=100))

    items = list(res.top(5).stream(page_size=2))

    assert [m.item_code for m in items] == [f"I{i:04d}" for i in range(5)]
    # $top must never reach SAP (it is enforced client-side).
    for call in res._adapter.get.call_args_list:  # type: ignore[attr-defined]
        assert "$top" not in (call.kwargs.get("ep_params") or {})


# ──────────────────────────────────────────────────────────────────────────────
# 5. execute() + $top — total cap (OData semantics): eager-fill across pages
# ──────────────────────────────────────────────────────────────────────────────

def test_execute_top_eager_fills_to_n_across_pages():
    # 280 rows, server page 20. top(100) must return 100 (not one 20-row page).
    res = _sync_resource(FakeServiceLayer(total=280))

    page = res.top(100).execute()

    assert isinstance(page, PaginatedResult)
    assert len(page) == 100
    assert page.has_more is True
    # The next cursor is the absolute skip after the returned rows, gap-free.
    assert page.next_skip == 100
    assert page.next_params == {"$skip": "100"}
    # The first page's @odata.context metadata is preserved through truncation.
    assert page.metadata == "$metadata#Items"
    # One row beyond the cap is needed to know more exist: ceil(101/20) = 6 GETs.
    assert res._adapter.get.call_count == 6  # type: ignore[attr-defined]
    # $top is enforced client-side and never sent to SAP.
    for call in res._adapter.get.call_args_list:  # type: ignore[attr-defined]
        assert "$top" not in (call.kwargs.get("ep_params") or {})


def test_execute_top_small_stays_single_request():
    # top <= one server page → still a single GET (regression guard).
    res = _sync_resource(FakeServiceLayer(total=100))

    page = res.top(5).execute()

    assert isinstance(page, PaginatedResult)
    assert len(page) == 5
    assert page.has_more is True
    assert page.next_skip == 5
    assert res._adapter.get.call_count == 1  # type: ignore[attr-defined]


def test_execute_top_exceeding_total_returns_all_and_stops():
    res = _sync_resource(FakeServiceLayer(total=50))

    page = res.top(100).execute()

    assert isinstance(page, PaginatedResult)
    assert len(page) == 50
    assert page.has_more is False
    assert page.next_skip is None


def test_execute_top_preserves_filter_and_skip_in_next_cursor():
    res = _sync_resource(FakeServiceLayer(total=280))

    page = res.filter(Item.frozen == False).skip(40).top(100).execute()  # noqa: E712

    assert isinstance(page, PaginatedResult)
    assert page.next_skip == 140  # base_skip(40) + top(100)
    assert page.next_params == {"$filter": "Frozen eq 'tNO'", "$skip": "140"}


def test_next_skip_on_plain_list_page_and_last_page():
    res = _sync_resource(FakeServiceLayer(total=100))

    page = res.list(query=ODataQuery(top=2))
    assert page.next_skip == 2  # mid-collection cursor

    last = res.list(query=ODataQuery(filter="ItemCode eq 'I0042'", top=5))
    assert last.next_skip is None  # single-page result


@pytest.mark.asyncio
async def test_async_execute_top_eager_fills_to_n():
    res = _async_resource(FakeServiceLayer(total=280))

    page = await res.top(100).execute()

    assert isinstance(page, PaginatedResult)
    assert len(page) == 100
    assert page.has_more is True
    assert page.next_skip == 100


@pytest.mark.asyncio
async def test_async_total_count_with_count_true():
    res = _async_resource(FakeServiceLayer(total=100))

    page = await res.list(query=ODataQuery(top=5, count=True))

    assert len(page) == 5
    assert page.total_count == 100


# ──────────────────────────────────────────────────────────────────────────────
# 6. @odata.count → total_count (opt-in via $count=true)
# ──────────────────────────────────────────────────────────────────────────────

def test_total_count_populated_with_count_true():
    res = _sync_resource(FakeServiceLayer(total=100))

    page = res.list(query=ODataQuery(top=5, count=True))

    assert len(page) == 5
    assert page.total_count == 100  # full result-set size, independent of paging


def test_total_count_respects_filter():
    # 3 tYES + 97 tNO; a tNO filter's count is 97, not 100.
    res = _sync_resource(FakeServiceLayer(total=100, frozen_count=3))

    page = res.list(query=ODataQuery(filter="Frozen eq 'tNO'", count=True))

    assert page.total_count == 97


def test_total_count_none_without_count_opt_in():
    res = _sync_resource(FakeServiceLayer(total=100))

    page = res.list(query=ODataQuery(top=5))

    assert page.total_count is None


# ──────────────────────────────────────────────────────────────────────────────
# Async parity
# ──────────────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_async_has_more_fencepost_and_stream():
    res = _async_resource(FakeServiceLayer(total=100))

    page = await res.top(2).execute()
    assert isinstance(page, PaginatedResult)
    assert len(page) == 2
    assert page.has_more is True

    items = []
    async for item in res.top(5).stream(page_size=2):
        items.append(item)
    assert [m.item_code for m in items] == [f"I{i:04d}" for i in range(5)]


@pytest.mark.asyncio
async def test_async_boolean_literal_rejected():
    res = _async_resource(FakeServiceLayer())
    with pytest.raises(B1ValidationError):
        await res.filter("Frozen eq true").top(1).execute()
