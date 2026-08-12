"""get_raw(): raw wire reads, the inbound counterpart of update(key, dict).

Together they close the verbatim loop (get_raw -> edit dict -> update(dict))
so byte-exact flows never need to touch ``client._adapter``.
"""
from __future__ import annotations

import pytest
from pydantic import Field as PydanticField

from b1sl.b1sl.models.base import B1Model, SapBool
from b1sl.b1sl.resources.async_base import AsyncGenericResource
from b1sl.b1sl.resources.base import GenericResource
from tests.fakes.fake_rest_adapter import FakeAsyncRestAdapter, FakeRestAdapter

# Wire fragment as SAP actually sends it: SAP-encoded strings + a field the
# model does not declare. get_raw must return it untouched; get() normalizes.
WIRE = {
    "CardCode": "C001",
    "Frozen": "tYES",
    "CreateDate": "/Date(1754611200000)/",
    "CampoNoModelado": "xyz",
}


class _Partner(B1Model):
    card_code: str | None = PydanticField(None, alias="CardCode")
    frozen: SapBool | None = PydanticField(None, alias="Frozen")


class _Partners(GenericResource[_Partner]):
    endpoint = "BusinessPartners"
    model = _Partner


class _AsyncPartners(AsyncGenericResource[_Partner]):
    endpoint = "BusinessPartners"
    model = _Partner


@pytest.fixture
def fake():
    f = FakeRestAdapter()
    f.register("GET", "BusinessPartners('C001')", response_data=dict(WIRE))
    return f


@pytest.fixture
def afake():
    f = FakeAsyncRestAdapter()
    f.register("GET", "BusinessPartners('C001')", response_data=dict(WIRE))
    return f


def test_get_raw_returns_wire_dict_untouched(fake):
    raw = _Partners(fake).get_raw("C001")
    assert raw == WIRE                        # no validator touched anything
    assert raw["Frozen"] == "tYES"            # still the SAP string, not True
    assert raw["CreateDate"] == "/Date(1754611200000)/"  # legacy format kept
    assert raw["CampoNoModelado"] == "xyz"    # unknown field present


def test_get_still_normalizes(fake):
    bp = _Partners(fake).get("C001")
    assert bp.frozen is True                  # same route, validated


def test_get_raw_passes_select_expand_headers(fake):
    fake.register("GET", "BusinessPartners('C001')", response_data=dict(WIRE))
    _Partners(fake).get_raw(
        "C001", select=["CardCode"], expand=["BPAddresses"], headers={"H": "1"}
    )
    call = fake.calls[-1]
    assert call["params"] == {"$select": "CardCode", "$expand": "BPAddresses"}
    assert call["headers"] == {"H": "1"}


def test_get_raw_then_update_dict_round_trip(fake):
    """The full verbatim loop: what came off the wire goes back unchanged."""
    fake.register("PATCH", "BusinessPartners('C001')", status=204)
    res = _Partners(fake)
    raw = res.get_raw("C001")
    raw["CampoNoModelado"] = "editado"
    res.update("C001", raw)
    sent = fake.calls[-1]["data"]
    assert sent["Frozen"] == "tYES"           # never became True/true
    assert sent["CreateDate"] == "/Date(1754611200000)/"
    assert sent["CampoNoModelado"] == "editado"


@pytest.mark.asyncio
async def test_async_get_raw_parity(afake):
    raw = await _AsyncPartners(afake).get_raw("C001")
    assert raw == WIRE
    assert raw["Frozen"] == "tYES"


@pytest.mark.asyncio
async def test_async_get_still_normalizes(afake):
    bp = await _AsyncPartners(afake).get("C001")
    assert bp.frozen is True
