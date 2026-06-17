from unittest.mock import MagicMock

import pytest

from b1sl.b1sl.async_rest_adapter import AsyncRestAdapter
from b1sl.b1sl.models.base import B1Model
from b1sl.b1sl.models.result import Result
from b1sl.b1sl.resources.async_base import AsyncGenericResource
from b1sl.b1sl.resources.base import GenericResource
from b1sl.b1sl.rest_adapter import RestAdapter


class MockModel(B1Model):
    item_code: str | None = None
    id: int | None = None

# ------------------------------------------------------------------------------
# SYNC STREAM TESTS
# ------------------------------------------------------------------------------

def test_sync_stream_multi_page():
    """Verify that .stream() fetches multiple pages correctly."""
    adapter = MagicMock(spec=RestAdapter)
    
    # Page 1: has nextLink
    res1 = Result(
        status_code=200,
        data={"value": [{"item_code": "A1"}, {"item_code": "A2"}]},
        next_link="https://localhost/b1s/v1/Items?$skip=2"
    )
    # Page 2: no nextLink
    res2 = Result(
        status_code=200,
        data={"value": [{"item_code": "A3"}]}
    )
    
    adapter.get.side_effect = [res1, res2]
    
    resource: GenericResource[MockModel] = GenericResource(adapter)
    resource.endpoint = "Items"
    resource.model = MockModel
    
    items = list(resource.stream())
    
    assert len(items) == 3
    assert items[0].item_code == "A1"
    assert items[1].item_code == "A2"
    assert items[2].item_code == "A3"
    assert adapter.get.call_count == 2

def test_sync_stream_max_pages():
    """Verify that .stream() respects the max_pages limit."""
    adapter = MagicMock(spec=RestAdapter)
    
    # Always provide a nextLink
    res = Result(
        status_code=200,
        data={"value": [{"item_code": "X"}]},
        next_link="https://localhost/b1s/v1/Items?$skip=1"
    )
    adapter.get.return_value = res
    
    resource: GenericResource[MockModel] = GenericResource(adapter)
    resource.endpoint = "Items"
    resource.model = MockModel
    
    # max_pages=3 should stop after 3 requests
    items = list(resource.stream(max_pages=3))
    
    assert len(items) == 3
    assert adapter.get.call_count == 3

def test_sync_stream_top_limit():
    """Verify that .top(N) acts as a hard limit across pages."""
    adapter = MagicMock(spec=RestAdapter)
    
    # Page 1: returns 2 items, but user only wants .top(3) and page_size=2
    res1 = Result(
        status_code=200,
        data={"value": [{"id": 1}, {"id": 2}]},
        next_link="https://localhost/b1s/v1/Items?$skip=2"
    )
    res2 = Result(
        status_code=200,
        data={"value": [{"id": 3}, {"id": 4}]}
    )
    adapter.get.side_effect = [res1, res2]
    
    resource: GenericResource[MockModel] = GenericResource(adapter)
    resource.endpoint = "Items"
    resource.model = MockModel
    
    # .top(3) should stop after yielding the 3rd item, potentially mid-page
    items = list(resource.top(3).stream(page_size=2))
    
    assert len(items) == 3
    assert [i.id for i in items] == [1, 2, 3]
    # It should have made 2 calls (to get the 3rd item)
    assert adapter.get.call_count == 2

def _make_stream_resource(adapter):
    resource: GenericResource[MockModel] = GenericResource(adapter)
    resource.endpoint = "Items"
    resource.model = MockModel
    return resource


def test_sync_stream_does_not_forward_top_to_sap():
    """$top must be enforced client-side and not forwarded to SAP. The mock
    simulates a strict SAP that drops the nextLink under any $top — proving the
    stream still pages correctly because we strip $top from the request."""
    adapter = MagicMock(spec=RestAdapter)

    def fake_get(endpoint, ep_params=None, data=None, headers=None):
        ep_params = ep_params or {}
        # Simulate SAP: omit nextLink whenever $top is present.
        if "$top" in ep_params:
            return Result(status_code=200, data={"value": [{"id": 1}, {"id": 2}]})
        skip = int(ep_params.get("$skip", 0))
        if skip == 0:
            return Result(
                status_code=200,
                data={"value": [{"id": 1}, {"id": 2}]},
                next_link="https://localhost/b1s/v1/Items?$skip=2",
            )
        return Result(status_code=200, data={"value": [{"id": 3}, {"id": 4}]})

    adapter.get.side_effect = fake_get
    resource = _make_stream_resource(adapter)

    items = list(resource.top(3).stream(page_size=2))

    # Crossed the page boundary and stopped at the global cap of 3.
    assert [i.id for i in items] == [1, 2, 3]
    # $top was never sent to SAP...
    for call in adapter.get.call_args_list:
        assert "$top" not in (call.kwargs.get("ep_params") or {})
    # ...and page_size went out as the B1S-PageSize header.
    assert adapter.get.call_args_list[0].kwargs["headers"] == {"B1S-PageSize": "2"}


def test_sync_builder_page_size_feeds_stream_and_arg_overrides():
    adapter = MagicMock(spec=RestAdapter)
    adapter.get.return_value = Result(status_code=200, data={"value": [{"id": 1}]})
    resource = _make_stream_resource(adapter)

    # Builder-level .page_size() is used when stream() gets no explicit arg.
    list(resource.page_size(7).stream())
    assert adapter.get.call_args.kwargs["headers"] == {"B1S-PageSize": "7"}

    # An explicit stream(page_size=...) argument wins over the builder setting.
    adapter.get.reset_mock()
    adapter.get.return_value = Result(status_code=200, data={"value": [{"id": 1}]})
    list(resource.page_size(7).stream(page_size=99))
    assert adapter.get.call_args.kwargs["headers"] == {"B1S-PageSize": "99"}


# ------------------------------------------------------------------------------
# ASYNC STREAM TESTS
# ------------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_async_stream_multi_page():
    """Verify that .stream() fetches multiple pages correctly in async mode."""
    adapter = MagicMock(spec=AsyncRestAdapter)
    
    res1 = Result(
        status_code=200,
        data={"value": [{"item_code": "A1"}]},
        next_link="https://localhost/b1s/v1/Items?$skip=2"
    )
    res2 = Result(
        status_code=200,
        data={"value": [{"item_code": "A2"}]}
    )
    adapter.get.side_effect = [res1, res2]
    
    resource: AsyncGenericResource[MockModel] = AsyncGenericResource(adapter)
    resource.endpoint = "Items"
    resource.model = MockModel
    
    items = []
    async for item in resource.stream():
        items.append(item)
        
    assert len(items) == 2
    assert adapter.get.call_count == 2

@pytest.mark.asyncio
async def test_async_stream_top_limit():
    """Verify that .top(N) acts as a hard limit across pages in async mode."""
    adapter = MagicMock(spec=AsyncRestAdapter)
    
    res1 = Result(status_code=200, data={"value": [{"id": 1}, {"id": 2}]}, next_link="https://localhost/b1s/v1/Items?$skip=2")
    adapter.get.return_value = res1 # Keep returning more
    
    resource: AsyncGenericResource[MockModel] = AsyncGenericResource(adapter)
    resource.endpoint = "Items"
    resource.model = MockModel
    
    items = []
    async for item in resource.top(1).stream():
        items.append(item)

    assert len(items) == 1
    assert adapter.get.call_count == 1


@pytest.mark.asyncio
async def test_async_stream_does_not_forward_top_to_sap():
    """Async parity: $top is enforced client-side, never sent to SAP."""
    adapter = MagicMock(spec=AsyncRestAdapter)

    async def fake_get(endpoint, ep_params=None, data=None, headers=None):
        ep_params = ep_params or {}
        if "$top" in ep_params:
            return Result(status_code=200, data={"value": [{"id": 1}, {"id": 2}]})
        skip = int(ep_params.get("$skip", 0))
        if skip == 0:
            return Result(
                status_code=200,
                data={"value": [{"id": 1}, {"id": 2}]},
                next_link="https://localhost/b1s/v1/Items?$skip=2",
            )
        return Result(status_code=200, data={"value": [{"id": 3}, {"id": 4}]})

    adapter.get.side_effect = fake_get

    resource: AsyncGenericResource[MockModel] = AsyncGenericResource(adapter)
    resource.endpoint = "Items"
    resource.model = MockModel

    items = []
    async for item in resource.top(3).stream(page_size=2):
        items.append(item)

    assert [i.id for i in items] == [1, 2, 3]
    for call in adapter.get.call_args_list:
        assert "$top" not in (call.kwargs.get("ep_params") or {})
