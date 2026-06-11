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
    assert isinstance(result.data, dict)
    assert result.data["value"][0]["ItemCode"] == "A1000"

    # Validamos el flujo de llamadas
    assert route_get.called
    assert route_get.call_count == 2
    assert route_login.called
    assert route_login.call_count == 1


@respx.mock
def test_adapter_count_returns_plain_text_body(adapter):
    """``GET <Entity>/$count`` returns a bare text/plain integer in OData v4.

    The adapter must fall back to the raw text body instead of raising
    'Bad JSON response' when the success body is not JSON.
    """
    from datetime import datetime, timedelta

    adapter.reuse_token = True
    adapter.is_session_active = True
    adapter.token_expiry = datetime.now() + timedelta(hours=1)

    # A bare "10856" happens to parse as a JSON number; a body that is not
    # valid JSON at all must fall back to the raw text instead of raising.
    respx.get("https://sap-host:50000/b1s/v2/Items/$count").mock(
        side_effect=[
            Response(200, text="10856", headers={"Content-Type": "text/plain"}),
            Response(200, text="OK; not json", headers={"Content-Type": "text/plain"}),
        ]
    )

    numeric = adapter.get("/Items/$count")
    assert numeric.status_code == 200
    assert int(numeric.data) == 10856
    assert numeric.next_link is None

    raw_text = adapter.get("/Items/$count")
    assert raw_text.status_code == 200
    assert raw_text.data == "OK; not json"


# ── ETag proactive invalidation (sync) ────────────────────────────────────────

def _activate_session(adapter):
    from datetime import datetime, timedelta

    adapter.reuse_token = True
    adapter.is_session_active = True
    adapter.token_expiry = datetime.now() + timedelta(hours=1)


@respx.mock
def test_sync_etag_cleared_after_patch_and_delete(adapter):
    """Contract step 3: successful PATCH/DELETE must clear the cached ETag."""
    _activate_session(adapter)

    respx.patch("https://sap-host:50000/b1s/v2/Items('A1')").mock(
        return_value=Response(204)
    )
    respx.delete("https://sap-host:50000/b1s/v2/Items('B2')").mock(
        return_value=Response(204)
    )

    adapter._etag_cache["/Items('A1')"] = '"v1"'
    adapter._etag_cache["/Items('B2')"] = '"v1"'

    adapter.patch("Items('A1')", data={"ItemName": "Updated"})
    assert "/Items('A1')" not in adapter._etag_cache

    adapter.delete("Items('B2')")
    assert "/Items('B2')" not in adapter._etag_cache


@respx.mock
def test_sync_etag_parent_cleared_after_bound_action(adapter):
    """A bound Action POST must clear the ETag cached under the keyed parent."""
    _activate_session(adapter)

    respx.post("https://sap-host:50000/b1s/v2/Orders(1)/Cancel").mock(
        return_value=Response(204)
    )
    adapter._etag_cache["/Orders(1)"] = '"v1"'

    adapter.post("Orders(1)/Cancel")
    assert "/Orders(1)" not in adapter._etag_cache


@respx.mock
def test_sync_etag_not_cleared_by_dry_run(adapter):
    """Dry Run simulates writes — the real ETag cache must stay untouched."""
    _activate_session(adapter)
    adapter._etag_cache["/Items('A1')"] = '"v1"'

    with adapter.dry_run():
        adapter.patch("Items('A1')", data={"ItemName": "Simulated"})

    assert adapter._etag_cache.get("/Items('A1')") == '"v1"'


# ── Session license release on close() ───────────────────────────────────────

@respx.mock
def test_close_releases_session_license(adapter):
    """close() must POST /Logout when a session is active (license release)."""
    _activate_session(adapter)

    logout_route = respx.post("https://sap-host:50000/b1s/v2/Logout").mock(
        return_value=Response(204)
    )

    adapter.close()

    assert logout_route.called
    assert adapter.is_session_active is False

    # Idempotent: a second close() must not retry the logout.
    adapter.close()
    assert logout_route.call_count == 1


@respx.mock
def test_close_without_session_skips_logout(adapter):
    """close() with no active session must not attempt a Logout call."""
    # No routes mocked: any HTTP call would fail loudly.
    adapter.is_session_active = False
    adapter.close()


# ── 401-retry preserves semantic exceptions ──────────────────────────────────

@respx.mock
def test_relogin_retry_preserves_semantic_exception(adapter):
    """After a 401 → re-login, a failing retry must map to the semantic
    exception (e.g. 404 → B1NotFoundError), not a generic B1Exception."""
    from b1sl.b1sl.exceptions.exceptions import B1NotFoundError

    _activate_session(adapter)

    respx.get("https://sap-host:50000/b1s/v2/Items('GONE')").mock(
        side_effect=[
            Response(401, json={"error": {"code": 301, "message": {"value": "Invalid session"}}}),
            Response(404, json={"error": {"code": -2028, "message": {"value": "No matching records found"}}}),
        ]
    )
    respx.post("https://sap-host:50000/b1s/v2/Login").mock(
        return_value=Response(200, json={"SessionId": "new", "SessionTimeout": 30})
    )

    with pytest.raises(B1NotFoundError):
        adapter.get("/Items('GONE')")


# ── post_batch: semantic mapping + re-login ──────────────────────────────────

@respx.mock
def test_post_batch_maps_semantic_exception(adapter):
    """A failing $batch request must raise the mapped semantic exception."""
    from b1sl.b1sl.exceptions.exceptions import B1ValidationError

    _activate_session(adapter)

    respx.post("https://sap-host:50000/b1s/v2/$batch").mock(
        return_value=Response(
            400, json={"error": {"code": 311, "message": {"value": "Malformed batch"}}}
        )
    )

    with pytest.raises(B1ValidationError, match="Malformed batch"):
        adapter.post_batch("--b--", {"Content-Type": "multipart/mixed; boundary=b"})


@respx.mock
def test_post_batch_relogin_on_401(adapter):
    """post_batch must re-login once on 401 and retry the batch request."""
    _activate_session(adapter)

    batch_route = respx.post("https://sap-host:50000/b1s/v2/$batch").mock(
        side_effect=[
            Response(401, json={"error": {"code": 301, "message": {"value": "Invalid session"}}}),
            Response(200, content="--b--", headers={"Content-Type": "multipart/mixed; boundary=b"}),
        ]
    )
    login_route = respx.post("https://sap-host:50000/b1s/v2/Login").mock(
        return_value=Response(200, json={"SessionId": "new", "SessionTimeout": 30})
    )

    response = adapter.post_batch("--b--", {"Content-Type": "multipart/mixed; boundary=b"})

    assert response.status_code == 200
    assert login_route.called
    assert batch_route.call_count == 2
