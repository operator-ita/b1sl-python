import pytest

from b1sl.b1sl import ODataQuery
from b1sl.b1sl.models._generated.entities.inventory import Item


@pytest.mark.vcr
def test_get_item_real(sap_client_vcr, test_data):
    """Layer 2 + 3: Real SAP integration test.

    Verifies that an Item exists in the real ERP using a code from the
    business test data fixture.
    """
    item_code = test_data.get_test_item("simple")

    # 1. Retrieve item
    item = sap_client_vcr.items.get(item_code)

    # 2. Validate real SAP response
    assert item.item_code == item_code
    assert hasattr(item, "item_name")


@pytest.mark.vcr
def test_list_items_real(sap_client_vcr):
    """Real SAP item listing integration test."""
    # 1. Execute against real Service Layer
    items = sap_client_vcr.items.list(query=ODataQuery(top=5))

    # 2. Validate pagination and data
    assert len(items) > 0
    assert isinstance(items[0], Item)
