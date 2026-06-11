"""UDOResource / AsyncUDOResource CRUD coverage (previously untested)."""
from __future__ import annotations

import pytest

from b1sl.b1sl.models.base import B1Model
from b1sl.b1sl.models.paginated_result import PaginatedResult
from b1sl.b1sl.resources.udo import AsyncUDOResource, UDOResource
from tests.fakes.fake_rest_adapter import FakeAsyncRestAdapter, FakeRestAdapter

TABLE = "U_CT_ASSETS"


@pytest.fixture
def fake():
    return FakeRestAdapter()


@pytest.fixture
def udo(fake):
    return UDOResource(fake, table_name=TABLE)


def test_udo_get_by_doc_entry(fake, udo):
    fake.register_entity(f"{TABLE}(7)", {"DocEntry": 7, "U_Name": "Printer"})
    record = udo.get(7)
    assert isinstance(record, B1Model)
    assert record.get("U_Name") == "Printer"


def test_udo_list_returns_paginated_result(fake, udo):
    fake.register_collection(TABLE, [{"DocEntry": 1}, {"DocEntry": 2}])
    page = udo.list()
    assert isinstance(page, PaginatedResult)
    assert len(page) == 2
    assert page.has_more is False


def test_udo_create_posts_payload(fake, udo):
    fake.register("POST", TABLE, response_data={"DocEntry": 9, "U_Name": "New"})
    created = udo.create(B1Model(udfs={"U_Name": "New"}))
    assert created.get("DocEntry") == 9
    assert fake.calls[-1]["data"]["U_Name"] == "New"


def test_udo_update_patches_by_doc_entry(fake, udo):
    fake.register("PATCH", f"{TABLE}(3)", response_data=None, status=204)
    udo.update(3, B1Model(udfs={"U_Name": "Renamed"}))
    call = fake.calls[-1]
    assert call["method"] == "PATCH"
    assert call["data"]["U_Name"] == "Renamed"


def test_udo_delete_by_doc_entry(fake, udo):
    fake.register("DELETE", f"{TABLE}(3)", response_data=None, status=204)
    udo.delete(3)
    assert fake.calls[-1]["method"] == "DELETE"


# ── Async parity ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_async_udo_round_trip():
    fake = FakeAsyncRestAdapter()
    udo = AsyncUDOResource(fake, table_name=TABLE)

    fake.register("GET", f"{TABLE}(7)", response_data={"DocEntry": 7})
    fake.register("GET", TABLE, response_data={"value": [{"DocEntry": 1}]})
    fake.register("POST", TABLE, response_data={"DocEntry": 9})
    fake.register("PATCH", f"{TABLE}(9)", response_data=None, status=204)
    fake.register("DELETE", f"{TABLE}(9)", response_data=None, status=204)

    assert (await udo.get(7)).get("DocEntry") == 7
    assert len(await udo.list()) == 1
    assert (await udo.create(B1Model(udfs={"U_X": "1"}))).get("DocEntry") == 9
    await udo.update(9, B1Model(udfs={"U_X": "2"}))
    await udo.delete(9)
    assert [c["method"] for c in fake.calls] == ["GET", "GET", "POST", "PATCH", "DELETE"]
