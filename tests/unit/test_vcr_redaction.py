"""Unit tests for the VCR response-body data scrubber (tests/conftest.py).

Guards the cassette-hygiene contract: a re-record must not re-leak real SAP
master data (item names, GL accounts, UDFs, …). Codes/enums/odata keys are kept
so cassettes still validate on replay.
"""
from typing import Any

from tests.conftest import _is_sensitive_field, _scrub_response_data


def test_sensitive_field_detection():
    for f in ("ItemName", "ForeignName", "CardName", "CostAccount",
              "BarCode", "FreeText", "Address", "Phone", "SupplierCatalogNo",
              "U_CustomField", "FactorDescription"):
        assert _is_sensitive_field(f), f

    for f in ("ItemCode", "DocEntry", "ItemType", "Frozen", "Valid",
              "Quantity", "@odata.context"):
        assert not _is_sensitive_field(f), f


def test_scrub_redacts_business_values_keeps_identifiers():
    body: dict[str, Any] = {
        "@odata.context": "https://host/$metadata#Items",
        "value": [
            {
                "ItemCode": "9990140071261",        # key — kept
                "ItemName": "RENTAS DE BODEGAS",     # name — redacted
                "ItemType": "itItems",               # enum — kept
                "Frozen": "tNO",                     # enum — kept
                "CostAccount": "501-001-001-001",    # account — redacted (field)
                "U_Secreto": "valor privado",        # UDF — dropped entirely
                "U_Numerico": 42,                    # UDF — dropped even if not str
                "Remarks": "nota interna",           # remark — redacted
            }
        ],
    }
    _scrub_response_data(body)
    item = body["value"][0]

    assert item["ItemCode"] == "9990140071261"   # identifier preserved
    assert item["ItemType"] == "itItems"
    assert item["Frozen"] == "tNO"
    assert item["ItemName"] == "[REDACTED]"
    assert item["CostAccount"] == "[REDACTED]"
    # UDFs are removed key-and-value: even the field NAMES are company-internal
    # schema metadata that must not land in a cassette.
    assert "U_Secreto" not in item
    assert "U_Numerico" not in item
    assert item["Remarks"] == "[REDACTED]"
    assert body["@odata.context"] == "https://host/$metadata#Items"  # untouched


def test_scrub_keeps_sap_enums_under_sensitive_field_names():
    # PaymentBlock/BlockDunning ("block") and AddressType ("address") match
    # sensitive hints but hold SAP enum literals — redacting them breaks model
    # validation on replay, so they must survive.
    body: dict[str, Any] = {
        "PaymentBlock": "tNO",
        "BlockDunning": "tYES",
        "AddressType": "bo_BillTo",
        "AddressName": "Bodega Norte",  # real string under same hint — redacted
    }
    _scrub_response_data(body)
    assert body["PaymentBlock"] == "tNO"
    assert body["BlockDunning"] == "tYES"
    assert body["AddressType"] == "bo_BillTo"
    assert body["AddressName"] == "[REDACTED]"


def test_scrub_redacts_account_pattern_in_non_sensitive_field():
    # A GL-account-shaped value is redacted even if the field name isn't on the
    # denylist (value-pattern scrub).
    body: dict[str, Any] = {"SomeField": "see 601-037-001-001 for detail"}
    _scrub_response_data(body)
    assert "601-037-001-001" not in body["SomeField"]
    assert "[REDACTED]" in body["SomeField"]


def test_scrub_handles_nested_objects_and_lists():
    body: dict[str, Any] = {
        "DocumentLines": [
            {"LineNum": 0, "ItemDescription": "secret line text"},
            {"LineNum": 1, "WarehouseCode": "01"},
        ],
    }
    _scrub_response_data(body)
    assert body["DocumentLines"][0]["ItemDescription"] == "[REDACTED]"
    assert body["DocumentLines"][0]["LineNum"] == 0          # numbers untouched
    assert body["DocumentLines"][1]["WarehouseCode"] == "01"  # code kept
