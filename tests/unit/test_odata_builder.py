from datetime import date, datetime, time
from unittest.mock import MagicMock

from b1sl.b1sl.fields._generated.entities.inventory import ItemFields
from b1sl.b1sl.resources.base import GenericResource
from b1sl.b1sl.rest_adapter import RestAdapter


class MockModel:
    @classmethod
    def model_validate(cls, data):
        return data


def test_odata_value_formatting():
    from b1sl.b1sl.resources.odata import format_odata_value
    
    assert format_odata_value("O'Brien") == "'O''Brien'"
    assert format_odata_value(date(2024, 1, 1)) == "'2024-01-01'"
    assert format_odata_value(datetime(2024, 1, 1, 12, 0, 0)) == "'2024-01-01T12:00:00'"
    assert format_odata_value(time(18, 30)) == "'18:30:00'"
    # SAP B1 booleans are BoYesNoEnum (tYES/tNO), never Edm.Boolean.
    assert format_odata_value(True) == "'tYES'"
    assert format_odata_value(False) == "'tNO'"
    assert format_odata_value(None) == "null"

def test_odata_field_operators():
    # Test basic comparisons
    assert str(ItemFields.item_code == "A001") == "ItemCode eq 'A001'"
    assert str(ItemFields.item_code != "A001") == "ItemCode ne 'A001'"
    assert str(ItemFields.quantity_on_stock > 10) == "QuantityOnStock gt 10"
    
    # Test date comparison
    assert str(ItemFields.valid_from >= date(2024, 1, 1)) == "ValidFrom ge '2024-01-01'"
    
    # Test path construction (/)
    from b1sl.b1sl.fields import ServiceCall as SC
    assert str(SC.item / ItemFields.item_code) == "Item/ItemCode"
    
    # Test string methods
    assert str(ItemFields.item_name.contains("Widget")) == "contains(ItemName, 'Widget')"
    assert str(ItemFields.item_name.startswith("Q")) == "startswith(ItemName, 'Q')"
    
    # Boolean fields are BoYesNoEnum — Python bools must render as tYES/tNO.
    assert str(ItemFields.frozen == True) == "Frozen eq 'tYES'"  # noqa: E712
    assert str(ItemFields.frozen == False) == "Frozen eq 'tNO'"  # noqa: E712

    # Test logic composition
    expr = (ItemFields.item_code == "A001") & (ItemFields.valid == "tYES")
    assert str(expr) == "(ItemCode eq 'A001' and Valid eq 'tYES')"
    
    expr_or = (ItemFields.item_code == "A001") | (ItemFields.item_code == "A002")
    assert str(expr_or) == "(ItemCode eq 'A001' or ItemCode eq 'A002')"

def test_query_builder_fluent_interface():
    adapter = MagicMock(spec=RestAdapter)
    from typing import Any
    resource: GenericResource[Any] = GenericResource(adapter)
    resource.endpoint = "Items"
    resource.model = MockModel
    
    # Configure mock responses
    adapter.get.side_effect = [
        MagicMock(data={"value": [{"ItemCode": "A001"}]}, next_link=None, metadata=None),
        MagicMock(data={"ItemCode": "A001", "ItemName": "Fluent Item"})
    ]
    
    # 1. Collection query
    results = resource.filter(ItemFields.item_code == "A001") \
                      .select(ItemFields.item_code, ItemFields.item_name) \
                      .top(5) \
                      .execute()
    
    assert len(results) == 1
    assert results[0]["ItemCode"] == "A001"
    
    # 2. Single entity fluent query
    item = resource.by_id("A001") \
                   .select(ItemFields.item_code, ItemFields.item_name) \
                   .execute()
    
    assert item["ItemCode"] == "A001"
    assert item["ItemName"] == "Fluent Item"
    
    # Verify adapter call for by_id
    args, kwargs = adapter.get.call_args_list[1]
    assert args[0] == "Items('A001')"
    assert kwargs["ep_params"] == {"$select": "ItemCode,ItemName"}

def test_odata_query_apply_in_params():
    from b1sl.b1sl.resources.base import ODataQuery
    q = ODataQuery(apply="aggregate(DocTotal with sum as Total)")
    params = q.to_params()
    assert params["$apply"] == "aggregate(DocTotal with sum as Total)"
    assert "$filter" not in params


def test_odata_query_apply_none_omitted():
    from b1sl.b1sl.resources.base import ODataQuery
    q = ODataQuery(filter="DocStatus eq 'O'")
    params = q.to_params()
    assert "$apply" not in params


def test_query_builder_apply_fluent():
    from typing import Any
    from unittest.mock import MagicMock
    adapter = MagicMock(spec=RestAdapter)
    adapter.get.return_value = MagicMock(
        data={"value": [{"TotalDocTotal": 42000}]}, next_link=None, metadata=None
    )
    resource: GenericResource[Any] = GenericResource(adapter)
    resource.endpoint = "Orders"
    resource.model = MockModel

    resource.apply("aggregate(DocTotal with sum as TotalDocTotal)").execute()

    call_params = adapter.get.call_args[1]["ep_params"]
    assert call_params["$apply"] == "aggregate(DocTotal with sum as TotalDocTotal)"
    assert "$filter" not in call_params


def test_query_builder_apply_with_filter():
    from typing import Any
    from unittest.mock import MagicMock
    adapter = MagicMock(spec=RestAdapter)
    adapter.get.return_value = MagicMock(
        data={"value": [{"CardCode": "c001", "Total": 8}]}, next_link=None, metadata=None
    )
    resource: GenericResource[Any] = GenericResource(adapter)
    resource.endpoint = "Orders"
    resource.model = MockModel

    expr = (
        "filter(DocStatus eq 'O')"
        "/groupby((CardCode), aggregate(DocNum with sum as Total))"
    )
    resource.apply(expr).execute()

    call_params = adapter.get.call_args[1]["ep_params"]
    assert call_params["$apply"] == expr


def test_query_builder_apply_count_virtual():
    from typing import Any
    from unittest.mock import MagicMock
    adapter = MagicMock(spec=RestAdapter)
    adapter.get.return_value = MagicMock(
        data={"value": [{"OrdersCount": 4}]}, next_link=None, metadata=None
    )
    resource: GenericResource[Any] = GenericResource(adapter)
    resource.endpoint = "Orders"
    resource.model = MockModel

    resource.apply("aggregate($count as OrdersCount)").execute()

    call_params = adapter.get.call_args[1]["ep_params"]
    assert call_params["$apply"] == "aggregate($count as OrdersCount)"


if __name__ == "__main__":
    # Manual check since I don't want to rely on the test runner for this quick validation
    test_odata_field_operators()
    print("OData Field Operators: OK")
    test_query_builder_fluent_interface()
    print("Query Builder Fluent Interface: OK")
