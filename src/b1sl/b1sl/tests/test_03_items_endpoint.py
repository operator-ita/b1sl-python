"""
test_03_items_resource.py — ItemsResource unit tests (pure pytest, no Django).

Renamed from test_03_items_endpoint.py which tested the deprecated endpoint
class and required Django. These tests mock RestAdapter so no live SAP
connection is needed.
"""

from unittest.mock import MagicMock

import pytest

from b1sl.b1sl.exceptions.exceptions import B1Exception
from b1sl.b1sl.models.item import Item
from b1sl.b1sl.models.result import Result
from b1sl.b1sl.resources.items import ItemsResource
from b1sl.b1sl.rest_adapter import RestAdapter


@pytest.fixture
def mock_adapter():
    adapter = MagicMock(spec=RestAdapter)
    return adapter


@pytest.fixture
def items(mock_adapter):
    return ItemsResource(adapter=mock_adapter)


# ── get() ────────────────────────────────────────────────────────────────── #


def test_get_returns_item(items, mock_adapter):
    mock_adapter.get.return_value = Result(
        status_code=200,
        message="OK",
        data={
            "ItemCode": "ITEM-001",
            "ItemName": "Widget",
            "Valid": True,
            "QuantityOnStock": 5.0,
        },
    )
    item = items.get("ITEM-001")
    assert isinstance(item, Item)
    assert item.item_code == "ITEM-001"
    assert item.item_name == "Widget"
    assert item.valid is True


def test_get_decodes_tyes_to_true(items, mock_adapter):
    mock_adapter.get.return_value = Result(
        status_code=200,
        message="OK",
        data={"ItemCode": "X", "Valid": "tYES"},
    )
    item = items.get("X")
    assert item.valid is True


def test_get_decodes_tno_to_false(items, mock_adapter):
    mock_adapter.get.return_value = Result(
        status_code=200,
        message="OK",
        data={"ItemCode": "X", "Valid": "tNO"},
    )
    item = items.get("X")
    assert item.valid is False


def test_get_with_custom_model(items, mock_adapter):
    from pydantic import Field

    from b1sl.b1sl.models.base import B1Model

    class CustomItem(B1Model):
        item_code: str = Field(alias="ItemCode")
        custom_udf: str | None = Field(None, alias="U_Custom")

    mock_adapter.get.return_value = Result(
        status_code=200,
        message="OK",
        data={"ItemCode": "X", "U_Custom": "hello"},
    )
    result = items.get("X", model=CustomItem)
    assert isinstance(result, CustomItem)
    assert result.custom_udf == "hello"


# ── list() ───────────────────────────────────────────────────────────────── #


def test_list_returns_paginated_result(items, mock_adapter):
    from b1sl.b1sl.models.paginated_result import PaginatedResult

    mock_adapter.get.return_value = Result(
        status_code=200,
        message="OK",
        data={
            "value": [
                {
                    "ItemCode": "A",
                    "ItemName": "Alpha",
                    "Valid": "tYES",
                    "QuantityOnStock": 1.0,
                },
                {
                    "ItemCode": "B",
                    "ItemName": "Beta",
                    "Valid": "tNO",
                    "QuantityOnStock": 0.0,
                },
            ]
        },
    )
    page = items.list()
    assert isinstance(page, PaginatedResult)
    rows = page.to_list()
    assert len(rows) == 2
    assert rows[0].item_code == "A"
    assert isinstance(rows[0], Item)  # default is now Item, not ItemPage
    assert rows[0].valid is True
    assert rows[1].valid is False


def test_list_empty_value_key(items, mock_adapter):
    mock_adapter.get.return_value = Result(
        status_code=200,
        message="OK",
        data={"value": []},
    )
    page = items.list()
    assert page.to_list() == []


# ── update() returns fresh GET after 204 ─────────────────────────────────── #


def test_update_re_fetches_item(items, mock_adapter):
    from pydantic import Field

    from b1sl.b1sl.models.base import B1Model

    class ItemUpdate(B1Model):
        valid: bool | None = Field(None, alias="Valid")

    mock_adapter.patch.return_value = Result(
        status_code=204, message="No Content", data=None
    )
    mock_adapter.get.return_value = Result(
        status_code=200,
        message="OK",
        data={"ItemCode": "X", "ItemName": "Updated", "Valid": True},
    )
    result = items.update("X", ItemUpdate(valid=True))
    assert result.item_name == "Updated"


def test_update_raises_on_unexpected_status(items, mock_adapter):
    from pydantic import Field

    from b1sl.b1sl.models.base import B1Model

    class ItemUpdate(B1Model):
        valid: bool | None = Field(None, alias="Valid")

    mock_adapter.patch.return_value = Result(
        status_code=200, message="OK", data={"ItemCode": "X"}
    )
    with pytest.raises(B1Exception):
        items.update("X", ItemUpdate(valid=True))
