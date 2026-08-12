"""BPAddresses PATCH semantics against a real Service Layer (VCR-recorded).

Pins the server-side behavior documented in docs/18-sap-version-quirks.md Q2
(SAP B1 2511, HANA): a default PATCH treats a BPAddresses member as an
in-place UPDATE only when the full identifier set is present
(BPCode + AddressName + AddressType + RowNum); with any of them missing the
member is an INSERT (append, or -2035 on an existing AddressName).
``replace_collections=True`` replaces the collection wholesale (the way to
delete rows).

Re-record with `make test-record` after a SAP upgrade — if any assertion
breaks, SAP changed the semantics and Q2 needs an update.

All data is synthetic: the test creates its own BP and deletes it at the end;
no pre-existing business data is read or written. Cassette scrubbing redacts
names/addresses/cities anyway, so assertions rely only on counts, RowNum and
error codes.
"""
import pytest

from b1sl.b1sl import entities as en
from b1sl.b1sl.exceptions.exceptions import B1ValidationError

CARD_CODE = "CTESTB1SLVCR"


def _addr(name: str, city: str) -> "en.BPAddress":
    return en.BPAddress(address_name=name, city=city, address_type="bo_BillTo")


@pytest.mark.vcr
def test_bp_addresses_patch_is_append_only_and_replace_flag_works(
    sap_client_record_aware,
):
    bps = sap_client_record_aware.business_partners

    # Leftover cleanup from a previous recording run (404 is fine and is
    # simply part of the recorded flow).
    try:
        bps.delete(CARD_CODE)
    except Exception:
        pass

    # 1. Create a throwaway BP with 3 synthetic addresses. The RFC is the
    # generic MX placeholder (required for domestic BPs on MX localization).
    bps.create(en.BusinessPartner(
        card_code=CARD_CODE,
        card_name="b1sl vcr addresses test",
        card_type="cCustomer",
        federal_tax_id="XAXX010101000",
        bp_addresses=[
            _addr("VCR-1", "CityOne"),
            _addr("VCR-2", "CityTwo"),
            _addr("VCR-3", "CityThree"),
        ],
    ))
    created = bps.get(CARD_CODE)
    assert len(created.bp_addresses or []) == 3

    # 2. Default PATCH with a NEW AddressName appends (no in-place merge).
    bps.update(CARD_CODE, en.BusinessPartner(
        bp_addresses=[_addr("VCR-4", "CityFour")],
    ))
    after_append = bps.get(CARD_CODE)
    assert len(after_append.bp_addresses or []) == 4

    # 3. Default PATCH with an EXISTING AddressName but an incomplete
    # identifier set fails -2035: SL tries to INSERT the member.
    with pytest.raises(B1ValidationError, match="-2035"):
        bps.update(CARD_CODE, en.BusinessPartner(
            bp_addresses=[_addr("VCR-4", "CityChanged")],
        ))

    # 3b. With the FULL identifier set (BPCode + AddressName + AddressType +
    # RowNum) the same default PATCH updates the row in place — sent here as a
    # verbatim dict payload (no model serialization). Row count and RowNum
    # values must be unchanged.
    rownums_before = {a.row_num for a in (after_append.bp_addresses or [])}
    target_rownum = max(rownums_before)  # the appended VCR-4 row
    bps.update(CARD_CODE, {
        "BPAddresses": [{
            "BPCode": CARD_CODE,
            "AddressName": "VCR-4",
            "AddressType": "bo_BillTo",
            "RowNum": target_rownum,
            "City": "CityPatched",
        }],
    })
    after_inplace = bps.get(CARD_CODE)
    assert len(after_inplace.bp_addresses or []) == 4
    assert {a.row_num for a in (after_inplace.bp_addresses or [])} == rownums_before

    # 4. replace_collections=True replaces the collection wholesale: the BP
    # ends up with exactly the 2 addresses sent. Rows sent WITHOUT RowNum are
    # re-inserted (RowNum values renumbered — do not rely on them).
    old_rownums = {a.row_num for a in (after_append.bp_addresses or [])}
    bps.update(
        CARD_CODE,
        en.BusinessPartner(bp_addresses=[
            _addr("VCR-A", "CityA"),
            _addr("VCR-B", "CityB"),
        ]),
        replace_collections=True,
    )
    after_replace = bps.get(CARD_CODE)
    assert len(after_replace.bp_addresses or []) == 2
    new_rownums = {a.row_num for a in (after_replace.bp_addresses or [])}
    assert new_rownums.isdisjoint(old_rownums)

    # 5. Cleanup.
    bps.delete(CARD_CODE)
    assert not bps.exists(CARD_CODE)
