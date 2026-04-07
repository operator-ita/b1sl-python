import pytest

from b1sl.b1sl import B1Client, B1Config

# Importamos desde el __init__ de entities para obtener los modelos ya reconstruidos
from b1sl.b1sl.models._generated.entities import Item
from b1sl.b1sl.resources.base import ODataQuery
from tests.fakes.fake_rest_adapter import FakeRestAdapter


@pytest.fixture
def fake_adapter():
    return FakeRestAdapter()


@pytest.fixture
def mock_client(fake_adapter):
    """
    Cliente inyectado con FakeRestAdapter para pruebas unitarias.
    """
    config = B1Config(
        base_url="https://sap-server.example.com/b1s/v2",
        username="manager",
        password="sap",
        company_db="SBODEMO",
    )
    return B1Client(config=config, adapter=fake_adapter)


def test_get_item_mock(mock_client, fake_adapter, mock_responses):
    """Prueba unitaria: GET Item usando snake_case attributes."""
    # 1. Preparar datos
    fake_json = mock_responses("items_single")
    fake_adapter.register("GET", "Items('9990140071261')", response_data=fake_json)

    # 2. Ejecutar
    item = mock_client.items.get("9990140071261")

    # 3. Validar - Las propiedades en el SDK son snake_case
    assert item.item_code == "9990140071261"
    assert item.item_name == "QUESO OAXACA PREMIUM"
    assert any("Items" in c["endpoint"] for c in fake_adapter.calls)


def test_list_items_mock(mock_client, fake_adapter, mock_responses):
    """Prueba unitaria: Listar items usando ODataQuery y snake_case."""
    # 1. Preparar datos
    fake_adapter.register("GET", "Items", response_data=mock_responses("items_list"))

    # 2. Ejecutar - list() devuelve una list[Item] directamente
    items = mock_client.items.list(query=ODataQuery(top=2))

    assert len(items) == 2
    assert items[0].item_name == "QUESO OAXACA PREMIUM"

    # 3. Validar la llamada
    assert fake_adapter.calls[0]["method"] == "GET"
    assert "Items" in fake_adapter.calls[0]["endpoint"]


def test_insufficient_stock_error(mock_client, fake_adapter):
    """Prueba unitaria: Validación de errores de SAP (Falta de Stock)."""
    from b1sl.b1sl.exceptions.exceptions import B1ValidationError
    from tests.fakes.fake_rest_adapter import SAPErrorFactory

    # 1. Preparar error simulado
    stock_error = SAPErrorFactory.insufficient_stock()
    error_exc = B1ValidationError(
        "SAP Error -2035: Fall below zero stock not allowed", details=stock_error
    )

    fake_adapter.register("PATCH", "Items('9990140071261')", raises=error_exc)

    # 2. Ejecutar y validar que la excepción se propaga
    with pytest.raises(B1ValidationError) as exc_info:
        # Usamos snake_case en el constructor del Item del SDK
        mock_client.items.update("9990140071261", Item(quantity_on_stock=-10.0))

    # 3. Validar el contenido del error
    assert "-2035" in str(exc_info.value)
    assert exc_info.value.details == stock_error
    assert fake_adapter.calls[0]["method"] == "PATCH"
