import pytest

from b1sl.b1sl.client import B1Client
from b1sl.b1sl.models._generated.entities.businesspartners import BusinessPartner
from b1sl.b1sl.models._generated.entities.inventory import Item
from tests.fakes.fake_rest_adapter import FakeRestAdapter


def test_get_item_returns_typed_model(
    b1_client_fake: B1Client, fake_adapter: FakeRestAdapter
) -> None:
    """Validate that GET /Items('A001') correctly returns an Item model instance."""
    # 1. Arrange: Register the response in the fake adapter
    mock_data = {"ItemCode": "A001", "ItemName": "Test Item"}
    # we normalize by removing leading slash in the adapter, so both work
    fake_adapter.register_entity("Items('A001')", mock_data)

    # 2. Act: Call the client (using .get as defined in GenericResource)
    item = b1_client_fake.items.get("A001")

    # 3. Assert: Verify types and data
    assert isinstance(item, Item)
    assert item.item_code == "A001"
    assert item.item_name == "Test Item"
    assert len(fake_adapter.calls) == 1
    assert fake_adapter.calls[0]["method"] == "GET"


def test_list_items_with_pagination(
    b1_client_fake: B1Client, fake_adapter: FakeRestAdapter
) -> None:
    """Validate that GET /Items returns a list of Item models."""
    # 1. Arrange
    mock_items = [
        {"ItemCode": "A001", "ItemName": "Item 1"},
        {"ItemCode": "A002", "ItemName": "Item 2"},
    ]
    fake_adapter.register_collection("Items", mock_items)

    # 2. Act (using .list as defined in GenericResource)
    items = b1_client_fake.items.list()

    # 3. Assert
    assert len(items) == 2
    assert all(isinstance(i, Item) for i in items)
    assert items[0].item_code == "A001"


def test_create_business_partner_posts_correct_payload(
    b1_client_fake: B1Client, fake_adapter: FakeRestAdapter
) -> None:
    """Validate that POST /BusinessPartners sends the correct JSON payload."""
    # 1. Arrange
    bp_to_create = BusinessPartner(card_code="C1", card_name="Client 1")
    fake_adapter.register(
        "POST", "BusinessPartners", response_data=bp_to_create.model_dump(by_alias=True)
    )

    # 2. Act
    b1_client_fake.business_partners.create(bp_to_create)

    # 3. Assert
    last_call = fake_adapter.calls[-1]
    assert last_call["method"] == "POST"
    assert last_call["endpoint"] == "BusinessPartners"
    assert last_call["data"]["CardCode"] == "C1"
    assert last_call["data"]["CardName"] == "Client 1"


def test_adapter_raises_error_on_unregistered_route(b1_client_fake: B1Client) -> None:
    """Verify that the FakeRestAdapter fails loudly if a route is not registered."""
    with pytest.raises(ValueError, match="No response registered for GET NonExistent"):
        # Accessing the adapter directly to simulate an unregistered call
        b1_client_fake._adapter.get("NonExistent")
