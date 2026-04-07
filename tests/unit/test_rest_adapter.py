import pytest
import respx
from httpx import Response

from b1sl.b1sl.config import B1Config
from b1sl.b1sl.models.result import Result
from b1sl.b1sl.rest_adapter import RestAdapter


@pytest.fixture
def config():
    return B1Config(
        base_url="https://sap-host:50000",
        username="manager",
        password="sap",
        company_db="SBODEMO",
    )


@pytest.fixture
def adapter(config):
    # reuse_token=True is required to enable the @handle_token login/re-login logic internally
    return RestAdapter.from_config(config)


@respx.mock
def test_adapter_auto_relogin_on_401(adapter):
    """
    Simula la resiliencia del RestAdapter ante la expiración de la sesión.
    Se espera:
    1. GET /Items -> Falla con HTTP 401
    2. POST /Login -> Éxito HTTP 200 (Auto re-login)
    3. GET /Items -> Éxito HTTP 200 (Retry de la petición original)
    """
    from datetime import datetime, timedelta

    adapter.reuse_token = True
    adapter.is_session_active = True
    adapter.token_expiry = datetime.now() + timedelta(hours=1)

    # 1. Petición original falla (Sesión expirada del lado de SAP)
    # Note: RestAdapter appends /b1s/v2 by default if not in path
    route_get = respx.get("https://sap-host:50000/b1s/v2/Items").mock(
        side_effect=[
            Response(
                401, json={"error": {"code": 301, "message": {"value": "Invalid session"}}}
            ),
            Response(200, json={"value": [{"ItemCode": "A1000", "ItemName": "Test Item"}]}),
        ]
    )

    # 2. Login de recuperación
    route_login = respx.post("https://sap-host:50000/b1s/v2/Login").mock(
        return_value=Response(200, json={"SessionId": "new-session-xyz"})
    )

    # Ejecutamos la llamada
    result = adapter.get("/Items")

    # Validamos que obtuvimos la data del retry exitoso
    assert isinstance(result, Result)
    assert result.status_code == 200
    assert result.data["value"][0]["ItemCode"] == "A1000"

    # Validamos el flujo de llamadas
    assert route_get.called
    assert route_get.call_count == 2
    assert route_login.called
    assert route_login.call_count == 1
