from unittest.mock import AsyncMock, MagicMock

import pytest

from b1sl.b1sl.models.base import B1Model
from b1sl.b1sl.models.result import Result
from b1sl.b1sl.resources.async_base import AsyncGenericResource
from b1sl.b1sl.resources.base import GenericResource


class MockModel(B1Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)
    @classmethod
    def model_validate(cls, data):
        return cls(**data)

# ------------------------------------------------------------------------------
# SYNC STREAM TESTS
# ------------------------------------------------------------------------------

def test_sync_stream_multi_page():
    """Verify that .stream() fetches multiple pages correctly."""
    adapter = MagicMock()
    
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
    adapter = MagicMock()
    
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
    adapter = MagicMock()
    
    # Page 1: returns 2 items, but user only wants .top(3) and page_size=2
    res1 = Result(
        status_code=200,
        data={"value": [{"id": 1}, {"id": 2}]},
        next_link="..."
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

# ------------------------------------------------------------------------------
# ASYNC STREAM TESTS
# ------------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_async_stream_multi_page():
    """Verify that .stream() fetches multiple pages correctly in async mode."""
    adapter = AsyncMock()
    
    res1 = Result(
        status_code=200,
        data={"value": [{"item_code": "A1"}]},
        next_link="next"
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
    adapter = AsyncMock()
    
    res1 = Result(status_code=200, data={"value": [{"id": 1}, {"id": 2}]}, next_link="...")
    adapter.get.return_value = res1 # Keep returning more
    
    resource: AsyncGenericResource[MockModel] = AsyncGenericResource(adapter)
    resource.endpoint = "Items"
    resource.model = MockModel
    
    items = []
    async for item in resource.top(1).stream():
        items.append(item)
        
    assert len(items) == 1
    assert adapter.get.call_count == 1
