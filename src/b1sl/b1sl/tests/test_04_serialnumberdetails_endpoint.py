"""
test_04_serial_numbers_resource.py — SerialNumbersResource unit tests (pure pytest).

Renamed from test_04_serialnumberdetails_endpoint.py which required Django.
All tests use a mocked RestAdapter — no live SAP connection required.
"""

from unittest.mock import MagicMock

import pytest

from b1sl.b1sl.exceptions.exceptions import B1Exception
from b1sl.b1sl.models.result import Result
from b1sl.b1sl.models.serialnumberdetail import SerialNumberDetails
from b1sl.b1sl.resources.serial_numbers import SerialNumbersResource
from b1sl.b1sl.rest_adapter import RestAdapter


@pytest.fixture
def mock_adapter():
    return MagicMock(spec=RestAdapter)


@pytest.fixture
def sn_resource(mock_adapter):
    return SerialNumbersResource(adapter=mock_adapter)


# ── get() ────────────────────────────────────────────────────────────────── #


def test_get_returns_serial_number_details(sn_resource, mock_adapter):
    mock_adapter.get.return_value = Result(
        status_code=200,
        message="OK",
        data={
            "DocEntry": 42,
            "ItemCode": "SN-001",
            "MfrSerialNo": "SN123",
            "ItemDescription": "Widget",
        },
    )
    result = sn_resource.get(42)
    assert isinstance(result, SerialNumberDetails)
    assert result.doc_entry == 42
    assert result.item_code == "SN-001"


def test_get_with_custom_model(sn_resource, mock_adapter):
    from pydantic import Field

    from b1sl.b1sl.models.base import B1Model

    class CustomSerial(B1Model):
        doc_entry: int = Field(alias="DocEntry")
        user_location: str | None = Field(None, alias="U_Ubicacion")

    mock_adapter.get.return_value = Result(
        status_code=200,
        message="OK",
        data={"DocEntry": 99, "U_Ubicacion": "K-11-2"},
    )
    result = sn_resource.get(99, model=CustomSerial)
    assert isinstance(result, CustomSerial)
    assert result.user_location == "K-11-2"


def test_get_wraps_b1exception(sn_resource, mock_adapter):
    mock_adapter.get.side_effect = B1Exception("SAP Error -2028: Not found")
    with pytest.raises(B1Exception, match="SerialNumbersResource.get"):
        sn_resource.get(1)


# ── list() ───────────────────────────────────────────────────────────────── #


def test_list_returns_paginated_result(sn_resource, mock_adapter):
    from b1sl.b1sl.models.paginated_result import PaginatedResult

    mock_adapter.get.return_value = Result(
        status_code=200,
        message="OK",
        data={
            "value": [
                {
                    "DocEntry": 1,
                    "ItemCode": "A",
                    "MfrSerialNo": "SNA",
                    "ItemDescription": "Alpha",
                },
                {
                    "DocEntry": 2,
                    "ItemCode": "B",
                    "MfrSerialNo": "SNB",
                    "ItemDescription": "Beta",
                },
            ]
        },
    )
    page = sn_resource.list()
    assert isinstance(page, PaginatedResult)
    rows = page.to_list()
    assert len(rows) == 2
    assert rows[0].doc_entry == 1
    assert rows[1].item_code == "B"


def test_list_empty(sn_resource, mock_adapter):
    mock_adapter.get.return_value = Result(
        status_code=200,
        message="OK",
        data={"value": []},
    )
    page = sn_resource.list()
    assert page.to_list() == []


# ── update() ─────────────────────────────────────────────────────────────── #


def test_update_re_fetches_on_204(sn_resource, mock_adapter):
    from b1sl.b1sl.models.base import B1Model

    class SerialNumberUpdateTest(B1Model):
        pass

    mock_adapter.patch.return_value = Result(
        status_code=204, message="No Content", data=None
    )
    mock_adapter.get.return_value = Result(
        status_code=200,
        message="OK",
        data={
            "DocEntry": 42,
            "ItemCode": "X",
            "MfrSerialNo": "SN-X",
            "ItemDescription": "Widget",
        },
    )
    result = sn_resource.update(42, SerialNumberUpdateTest())
    assert result.doc_entry == 42


def test_update_raises_on_unexpected_status(sn_resource, mock_adapter):
    from b1sl.b1sl.models.base import B1Model

    class SerialNumberUpdateTest(B1Model):
        pass

    mock_adapter.patch.return_value = Result(
        status_code=200, message="OK", data={"DocEntry": 42}
    )
    with pytest.raises(B1Exception):
        sn_resource.update(42, SerialNumberUpdateTest())


# ── PaginatedResult.to_list() caching ────────────────────────────────────── #


def test_paginated_result_to_list_caches(sn_resource, mock_adapter):
    """to_list() must return the same list object on repeated calls."""
    mock_adapter.get.return_value = Result(
        status_code=200,
        message="OK",
        data={
            "value": [
                {
                    "DocEntry": 1,
                    "ItemCode": "A",
                    "MfrSerialNo": "S",
                    "ItemDescription": "D",
                }
            ]
        },
    )
    page = sn_resource.list()
    first = page.to_list()
    second = page.to_list()
    assert first is second, "to_list() is not returning cached list"
    third = list(page.data)
    assert third == first, "data property does not replay cache"
