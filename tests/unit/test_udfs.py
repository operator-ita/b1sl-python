import warnings
from unittest.mock import AsyncMock, MagicMock

import pytest

from b1sl.b1sl.models._generated.entities.general import UserFieldMD
from b1sl.b1sl.models.base import B1Model
from b1sl.b1sl.resources.async_base import AsyncGenericResource
from b1sl.b1sl.resources.base import GenericResource
from b1sl.b1sl.schemas.udf import UDFSchema


class MockItem(B1Model):
    item_code: str = "A001"

def test_udfs_read_capability():
    # Simulate inbound JSON from SAP
    payload = {
        "item_code": "A001",
        "U_CustomField": "CustomValue",
        "U_Number": 42
    }
    item = MockItem.model_validate(payload)
    
    # UDFs should be accessible via the mapping
    assert item.udfs["U_CustomField"] == "CustomValue"
    assert item.udfs["U_Number"] == 42
    assert len(item.udfs) == 2
    
    # Fallback access should still work
    assert item.get("U_CustomField") == "CustomValue"
    
def test_udfs_write_capability():
    item = MockItem(item_code="A001")
    
    # Setting values via mapping modifies the extra dict
    item.udfs["U_NewField"] = "NewValue"
    assert item.udfs["U_NewField"] == "NewValue"
    if item.model_extra is not None:
        assert item.model_extra["U_NewField"] == "NewValue"
    
    # Iteration
    keys = list(item.udfs)
    assert keys == ["U_NewField"]

    # Deleting
    del item.udfs["U_NewField"]
    assert "U_NewField" not in item.udfs
    assert len(item.udfs) == 0
    
def test_udfs_strict_enforcement():
    item = MockItem(item_code="A001")
    
    with pytest.raises(KeyError, match="only supports 'U_' keys"):
        item.udfs["InvalidField"] = "Value"
        
    with pytest.raises(KeyError, match="only supports 'U_' keys"):
        _ = item.udfs["InvalidField"]
    
    with pytest.raises(KeyError, match="only supports 'U_' keys"):
        del item.udfs["InvalidField"]

def test_udfs_constructor_injection():
    # Pass udfs explicitly during construction
    item = MockItem(item_code="A001", udfs={"U_Injected": "InjectedValue"})
    assert item.udfs["U_Injected"] == "InjectedValue"
    
    # Validate it serializes correctly to root level
    payload = item.to_api_payload()
    assert payload["U_Injected"] == "InjectedValue"
    assert "udfs" not in payload

def test_udfs_constructor_warning():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # Conflict: top-level U_ conflict with udfs parameter
        item = MockItem.model_validate({
            "item_code": "A001", 
            "U_Conflict": "TopLevel", 
            "udfs": {"U_Conflict": "UDFDict"}
        })
        
        assert len(w) == 1
        assert issubclass(w[-1].category, RuntimeWarning)
        assert "Constructor conflict" in str(w[-1].message)
        
        # udfs arg overwrites top-level
        assert item.udfs["U_Conflict"] == "UDFDict"

def test_udfs_validation_error():
    # Passing invalid UDF key in constructor throws ValueError
    with pytest.raises(ValueError, match="must start with 'U_'"):
        MockItem.model_validate({"item_code": "A001", "udfs": {"InvalidField": 1}})

def test_serialization():
    item = MockItem(item_code="A001")
    item.udfs["U_Custom"] = "Test"
    
    payload = item.to_api_payload()
    
    # The UDF should be at the root of the payload
    assert payload["U_Custom"] == "Test"
    assert payload["item_code"] == "A001"


def test_sync_get_udf_schema():
    # Setup mock adapter
    mock_adapter = MagicMock()
    mock_response = MagicMock()
    mock_response.data = {"value": [{"Name": "Segmento", "Type": "db_Alpha", "Size": 10}]}
    mock_adapter.get.return_value = mock_response
    
    # Instance resource
    res: GenericResource[MockItem] = GenericResource(mock_adapter)
    res.endpoint = "BusinessPartners"
    res.model = MockItem
    
    # Call method
    schema = res.get_udf_schema()
    
    # Verify
    mock_adapter.get.assert_called_with("UserFieldsMD", ep_params={"$filter": "TableName eq 'OCRD'"})
    assert "U_Segmento" in schema
    assert schema["U_Segmento"].name == "Segmento"
    
    # Test generation of pydantic model
    DynamicModel = schema.to_pydantic_model()
    # Pydantic should be able to instantiate it with keyword args matching the aliases
    instance = DynamicModel(**{"U_Segmento": "abc"})
    assert instance.model_dump(by_alias=True, exclude_none=True) == {"U_Segmento": "abc"}

@pytest.mark.asyncio
async def test_async_get_udf_schema():
    # Setup mock adapter
    mock_adapter = AsyncMock()
    mock_response = MagicMock()
    mock_response.data = {"value": [{"Name": "U_Priority", "Type": "db_Numeric", "Size": 2}]}
    mock_adapter.get.return_value = mock_response
    
    # Instance resource
    res: AsyncGenericResource[MockItem] = AsyncGenericResource(mock_adapter)
    res.endpoint = "Items"
    res.model = MockItem
    
    # Call method
    schema = await res.get_udf_schema()
    
    # Verify
    mock_adapter.get.assert_called_with("UserFieldsMD", ep_params={"$filter": "TableName eq 'OITM'"})
    assert "U_Priority" in schema
    assert schema["U_Priority"].name == "U_Priority"

def test_udf_schema_prefix_normalization():
    """Verify that names without the 'U_' prefix are normalised to include it."""
    
    # 1. Simulate a SAP response that omits the 'U_' prefix on some fields
    raw_udfs = [
        UserFieldMD(Name="CampoSinPrefijo", Type="db_Alpha", Description="Test 1"),
        UserFieldMD(Name="U_CampoConPrefijo", Type="db_Numeric", Description="Test 2")
    ]
    
    schema = UDFSchema("OCRD", raw_udfs)
    
    # Both must be accessible via 'U_' prefix
    assert "U_CampoSinPrefijo" in schema
    assert "U_U_CampoConPrefijo" not in schema  # prefix must not be duplicated
    assert "U_CampoConPrefijo" in schema
    
    # Verificar que el modelo Pydantic generado use las llaves normalizadas
    data = {"U_CampoSinPrefijo": "val", "U_CampoConPrefijo": 10}
    
    # validate_and_dump must work correctly with normalised keys
    payload = schema.validate_and_dump(data)
    assert payload["U_CampoSinPrefijo"] == "val"
    assert payload["U_CampoConPrefijo"] == 10
