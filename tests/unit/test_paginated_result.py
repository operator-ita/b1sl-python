"""Contract tests for PaginatedResult and the list()/execute() page API."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from b1sl.b1sl.async_rest_adapter import AsyncRestAdapter
from b1sl.b1sl.models.base import B1Model
from b1sl.b1sl.models.paginated_result import PaginatedResult
from b1sl.b1sl.models.result import Result
from b1sl.b1sl.resources.async_base import AsyncGenericResource
from b1sl.b1sl.resources.base import GenericResource, ODataQuery
from b1sl.b1sl.rest_adapter import RestAdapter


class MockModel(B1Model):
    item_code: str | None = None
    id: int | None = None


def _make_resource(adapter) -> GenericResource[MockModel]:
    resource: GenericResource[MockModel] = GenericResource(adapter)
    resource.endpoint = "Items"
    resource.model = MockModel
    return resource


def _make_async_resource(adapter) -> AsyncGenericResource[MockModel]:
    resource: AsyncGenericResource[MockModel] = AsyncGenericResource(adapter)
    resource.endpoint = "Items"
    resource.model = MockModel
    return resource


# ------------------------------------------------------------------------------
# Sequence semantics
# ------------------------------------------------------------------------------

def test_paginated_result_behaves_like_a_list():
    page = PaginatedResult([1, 2, 3], next_params={"$skip": "3"})

    assert len(page) == 3
    assert page[0] == 1
    assert page[-1] == 3
    assert page[:2] == [1, 2]
    assert list(page) == [1, 2, 3]
    assert [x for x in page] == [1, 2, 3]
    assert 2 in page
    assert page == [1, 2, 3]
    assert page == PaginatedResult([1, 2, 3])


def test_paginated_result_metadata_fields():
    last_page = PaginatedResult(["a"], metadata="$metadata#Items")
    assert last_page.metadata == "$metadata#Items"
    assert last_page.next_params is None
    assert last_page.has_more is False

    mid_page = PaginatedResult(["a"], next_params={"$skip": "20"})
    assert mid_page.has_more is True
    assert "has_more=True" in repr(mid_page)


def test_paginated_result_to_list_returns_fresh_copy():
    page = PaginatedResult([1, 2])
    materialised = page.to_list()
    assert materialised == [1, 2]
    materialised.append(3)
    assert len(page) == 2  # internal data untouched


def test_paginated_result_iterates_repeatedly():
    page = PaginatedResult([1, 2])
    assert list(page) == [1, 2]
    assert list(page) == [1, 2]  # no one-shot generator semantics


# ------------------------------------------------------------------------------
# Sync list()
# ------------------------------------------------------------------------------

def test_sync_list_returns_paginated_result_with_next_params():
    adapter = MagicMock(spec=RestAdapter)
    adapter.get.return_value = Result(
        status_code=200,
        data={"value": [{"item_code": "A1"}, {"item_code": "A2"}]},
        next_link="https://localhost/b1s/v1/Items?$skip=2",
        metadata="$metadata#Items",
    )
    resource = _make_resource(adapter)

    page = resource.list(query=ODataQuery(filter="ItemCode ne ''", top=2))

    assert isinstance(page, PaginatedResult)
    assert len(page) == 2
    assert page[0].item_code == "A1"
    assert page.metadata == "$metadata#Items"
    assert page.has_more is True
    # $skip comes from the nextLink; the original filter must survive
    assert page.next_params is not None
    assert page.next_params["$skip"] == "2"
    assert page.next_params["$filter"] == "ItemCode ne ''"


def test_sync_list_last_page_has_no_next_params():
    adapter = MagicMock(spec=RestAdapter)
    adapter.get.return_value = Result(
        status_code=200, data={"value": [{"item_code": "A1"}]}
    )
    resource = _make_resource(adapter)

    page = resource.list()

    assert page.next_params is None
    assert page.has_more is False


def test_sync_list_accepts_next_params_for_following_page():
    adapter = MagicMock(spec=RestAdapter)
    adapter.get.side_effect = [
        Result(
            status_code=200,
            data={"value": [{"item_code": "A1"}]},
            next_link="https://localhost/b1s/v1/Items?$skip=1",
        ),
        Result(status_code=200, data={"value": [{"item_code": "A2"}]}),
    ]
    resource = _make_resource(adapter)

    first_page = resource.list()
    second_page = resource.list(params=first_page.next_params)

    assert second_page[0].item_code == "A2"
    assert second_page.has_more is False
    assert adapter.get.call_args.kwargs["ep_params"] == {"$skip": "1"}


def test_sync_list_rejects_query_and_params_together():
    resource = _make_resource(MagicMock())
    with pytest.raises(ValueError, match="not both"):
        resource.list(query=ODataQuery(top=1), params={"$skip": "1"})


# ------------------------------------------------------------------------------
# $top fence-post — has_more detection when SAP omits @odata.nextLink
# ------------------------------------------------------------------------------

def test_top_probe_requests_one_extra_and_detects_more():
    # SAP returns top+1 rows and NO nextLink (its behaviour when $top is set).
    adapter = MagicMock(spec=RestAdapter)
    adapter.get.return_value = Result(
        status_code=200,
        data={"value": [{"item_code": f"A{i}"} for i in range(3)]},  # top(2) -> probe 3
    )
    resource = _make_resource(adapter)

    page = resource.list(query=ODataQuery(filter="Properties64 eq 'tYES'", top=2))

    # Probe asked for top+1...
    assert adapter.get.call_args.kwargs["ep_params"]["$top"] == "3"
    # ...but the extra row is truncated away.
    assert len(page) == 2
    assert [m.item_code for m in page] == ["A0", "A1"]
    # has_more is True even though SAP gave us no nextLink.
    assert page.has_more is True
    assert page.next_params is not None
    assert page.next_params["$skip"] == "2"
    assert page.next_params["$top"] == "2"  # original cap preserved for page 2
    assert page.next_params["$filter"] == "Properties64 eq 'tYES'"


def test_top_probe_last_page_reports_no_more():
    # Fewer than top+1 rows come back -> genuinely the last page.
    adapter = MagicMock(spec=RestAdapter)
    adapter.get.return_value = Result(
        status_code=200,
        data={"value": [{"item_code": "A0"}, {"item_code": "A1"}]},  # top(5) -> only 2
    )
    resource = _make_resource(adapter)

    page = resource.list(query=ODataQuery(top=5))

    assert adapter.get.call_args.kwargs["ep_params"]["$top"] == "6"
    assert len(page) == 2
    assert page.has_more is False
    assert page.next_params is None


def test_top_probe_advances_skip_cursor_for_following_page():
    adapter = MagicMock(spec=RestAdapter)
    adapter.get.return_value = Result(
        status_code=200,
        data={"value": [{"item_code": f"A{i}"} for i in range(3)]},
    )
    resource = _make_resource(adapter)

    # Caller already on page 2 (skip=2); next cursor must be skip + top.
    page = resource.list(params={"$top": "2", "$skip": "2"})

    assert len(page) == 2
    assert page.has_more is True
    assert page.next_params is not None
    assert page.next_params["$skip"] == "4"


def test_no_top_leaves_request_untouched():
    adapter = MagicMock(spec=RestAdapter)
    adapter.get.return_value = Result(
        status_code=200, data={"value": [{"item_code": "A0"}]}
    )
    resource = _make_resource(adapter)

    resource.list(query=ODataQuery(filter="ItemCode ne ''"))

    assert "$top" not in adapter.get.call_args.kwargs["ep_params"]


@pytest.mark.asyncio
async def test_async_top_probe_detects_more():
    adapter = MagicMock(spec=AsyncRestAdapter)
    adapter.get.return_value = Result(
        status_code=200,
        data={"value": [{"item_code": f"A{i}"} for i in range(3)]},
    )
    resource = _make_async_resource(adapter)

    page = await resource.list(query=ODataQuery(top=2))

    assert adapter.get.call_args.kwargs["ep_params"]["$top"] == "3"
    assert len(page) == 2
    assert page.has_more is True
    assert page.next_params is not None
    assert page.next_params["$skip"] == "2"


# ------------------------------------------------------------------------------
# page_size — B1S-PageSize header
# ------------------------------------------------------------------------------

def test_page_size_builder_sets_b1s_pagesize_header():
    adapter = MagicMock(spec=RestAdapter)
    adapter.get.return_value = Result(status_code=200, data={"value": [{"item_code": "A1"}]})
    resource = _make_resource(adapter)

    resource.page_size(50).execute()

    assert adapter.get.call_args.kwargs["headers"] == {"B1S-PageSize": "50"}


def test_list_page_size_param_sets_header():
    adapter = MagicMock(spec=RestAdapter)
    adapter.get.return_value = Result(status_code=200, data={"value": []})
    resource = _make_resource(adapter)

    resource.list(page_size=25)

    assert adapter.get.call_args.kwargs["headers"] == {"B1S-PageSize": "25"}


def test_list_without_page_size_sends_no_header():
    adapter = MagicMock(spec=RestAdapter)
    adapter.get.return_value = Result(status_code=200, data={"value": []})
    resource = _make_resource(adapter)

    resource.list()

    assert adapter.get.call_args.kwargs["headers"] is None


@pytest.mark.asyncio
async def test_async_page_size_builder_sets_header():
    adapter = MagicMock(spec=AsyncRestAdapter)
    adapter.get.return_value = Result(status_code=200, data={"value": []})
    resource = _make_async_resource(adapter)

    await resource.page_size(50).execute()

    assert adapter.get.call_args.kwargs["headers"] == {"B1S-PageSize": "50"}


# ------------------------------------------------------------------------------
# total_count — @odata.count exposure
# ------------------------------------------------------------------------------

def test_total_count_propagates_on_list():
    adapter = MagicMock(spec=RestAdapter)
    adapter.get.return_value = Result(
        status_code=200, data={"value": [{"item_code": "A1"}]}, total_count=273
    )
    page = _make_resource(adapter).list()
    assert page.total_count == 273


def test_total_count_is_none_when_not_requested():
    adapter = MagicMock(spec=RestAdapter)
    adapter.get.return_value = Result(status_code=200, data={"value": []})
    page = _make_resource(adapter).list()
    assert page.total_count is None


def test_total_count_captured_from_first_page_on_eager_top():
    adapter = MagicMock(spec=RestAdapter)
    adapter.get.side_effect = [
        Result(
            status_code=200,
            data={"value": [{"item_code": "A0"}, {"item_code": "A1"}]},
            next_link="https://localhost/b1s/v1/Items?$skip=2",
            total_count=10,  # only the first page carries @odata.count
        ),
        Result(status_code=200, data={"value": [{"item_code": "A2"}, {"item_code": "A3"}]}),
    ]
    page = _make_resource(adapter).top(3).execute()
    assert isinstance(page, PaginatedResult)
    assert len(page) == 3
    assert page.total_count == 10


def test_extract_odata_count_tolerates_v3_v4_and_missing():
    from b1sl.b1sl.pagination import extract_odata_count

    assert extract_odata_count({"@odata.count": 42}) == 42   # v4
    assert extract_odata_count({"odata.count": "7"}) == 7     # v3, string
    assert extract_odata_count({"value": []}) is None         # absent
    assert extract_odata_count({"@odata.count": "x"}) is None  # non-numeric


# ------------------------------------------------------------------------------
# QueryBuilder integration
# ------------------------------------------------------------------------------

def test_query_builder_execute_returns_paginated_result():
    adapter = MagicMock(spec=RestAdapter)
    adapter.get.return_value = Result(
        status_code=200,
        data={"value": [{"item_code": "A1"}]},
        next_link="https://localhost/b1s/v1/Items?$skip=1",
    )
    resource = _make_resource(adapter)

    page = resource.filter("ItemCode ne ''").execute()

    assert isinstance(page, PaginatedResult)
    assert page.has_more is True


def test_query_builder_first_returns_model_or_none():
    adapter = MagicMock(spec=RestAdapter)
    adapter.get.return_value = Result(
        status_code=200, data={"value": [{"item_code": "A1"}]}
    )
    resource = _make_resource(adapter)
    found = resource.filter("ItemCode ne ''").first()
    assert found is not None
    assert found.item_code == "A1"

    adapter.get.return_value = Result(status_code=200, data={"value": []})
    missing = resource.filter("ItemCode eq 'NOPE'").first()
    assert missing is None


# ------------------------------------------------------------------------------
# Async parity
# ------------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_async_list_returns_paginated_result_with_next_params():
    adapter = MagicMock(spec=AsyncRestAdapter)
    adapter.get.return_value = Result(
        status_code=200,
        data={"value": [{"item_code": "A1"}]},
        next_link="https://localhost/b1s/v1/Items?$skip=1",
    )
    resource = _make_async_resource(adapter)

    page = await resource.list()

    assert isinstance(page, PaginatedResult)
    assert page.next_params is not None
    assert page.next_params["$skip"] == "1"


@pytest.mark.asyncio
async def test_async_list_accepts_next_params_for_following_page():
    adapter = MagicMock(spec=AsyncRestAdapter)
    adapter.get.side_effect = [
        Result(
            status_code=200,
            data={"value": [{"item_code": "A1"}]},
            next_link="https://localhost/b1s/v1/Items?$skip=1",
        ),
        Result(status_code=200, data={"value": [{"item_code": "A2"}]}),
    ]
    resource = _make_async_resource(adapter)

    first_page = await resource.list()
    second_page = await resource.list(params=first_page.next_params)

    assert second_page[0].item_code == "A2"
    assert second_page.has_more is False


@pytest.mark.asyncio
async def test_async_list_rejects_query_and_params_together():
    resource = _make_async_resource(AsyncMock())
    with pytest.raises(ValueError, match="not both"):
        await resource.list(query=ODataQuery(top=1), params={"$skip": "1"})


@pytest.mark.asyncio
async def test_async_query_builder_first_returns_model_or_none():
    adapter = MagicMock(spec=AsyncRestAdapter)
    adapter.get.return_value = Result(
        status_code=200, data={"value": [{"item_code": "A1"}]}
    )
    resource = _make_async_resource(adapter)
    found = await resource.filter("ItemCode ne ''").first()
    assert found is not None
    assert found.item_code == "A1"

    adapter.get.return_value = Result(status_code=200, data={"value": []})
    missing = await resource.filter("ItemCode eq 'NOPE'").first()
    assert missing is None
