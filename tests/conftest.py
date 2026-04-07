import re
import sys
from typing import Any

import pytest

from b1sl.b1sl.client import B1Client
from b1sl.b1sl.config import B1Config
from tests.fakes.fake_rest_adapter import FakeRestAdapter

# ── Mock hdbcli (SAP HANA driver) ──────────────────────────────────────────
# This is always mocked at the top level to avoid installation requirements
_hdbcli_mock = type("MockHdbcli", (), {"dbapi": type("MockDbApi", (), {})})
sys.modules.setdefault("hdbcli", _hdbcli_mock)
sys.modules.setdefault("hdbcli.dbapi", _hdbcli_mock.dbapi)


@pytest.fixture
def fake_adapter() -> FakeRestAdapter:
    """Fixture providing a clean FakeRestAdapter instance for unit tests."""
    return FakeRestAdapter()


@pytest.fixture
def b1_client_fake(fake_adapter: FakeRestAdapter) -> B1Client:
    """Fixture providing a B1Client configured with the fake adapter.

    Returns:
        B1Client: An initialized client that won't make network calls.
    """
    config = B1Config(
        base_url="https://sap-server.example.com/b1s/v2",
        company_db="SBODemoMX",
        username="manager",
        password="sap",
    )
    client = B1Client(
        config=config,
        adapter=fake_adapter,
    )
    return client


@pytest.fixture(scope="session")
def vcr_config() -> dict[str, Any]:
    """Global VCR configuration with manual scrubbing for total privacy.

    Ensures that real hostnames and credentials are replaced with placeholders
    in the recorded cassettes.
    """

    def before_record_request_cb(request: Any) -> Any:
        # 1. Obfuscate the real Host in the recorded URI
        # We replace both common production-like domains and session tokens
        placeholder_host = "sap-server.example.com"

        # Replace hostname in URI
        import re

        request.uri = re.sub(
            r"https?://[^/]+", f"https://{placeholder_host}", request.uri
        )

        # 3. Sanitize Request Body (especially Login credentials)
        if request.body:
            try:
                import json

                body_str = request.body.decode("utf-8")
                # Try to parse as JSON
                data = json.loads(body_str)

                # Define keys to redact
                to_redact = {"password", "companydb", "company_db"}
                modified = False

                for key in data:
                    if key.lower() in to_redact:
                        data[key] = "[REDACTED]"
                        modified = True

                if modified:
                    request.body = json.dumps(data).encode("utf-8")
            except (UnicodeDecodeError, json.JSONDecodeError, TypeError):
                # Not a JSON body or not decodable, skip
                pass

        return request

    def before_record_response_cb(response: Any) -> Any:
        # 1. Redact response headers
        headers = response.get("headers", {})
        sensitive_headers = {"set-cookie", "cookie", "authorization", "b1session"}
        for header_name in list(headers.keys()):
            if header_name.lower() in sensitive_headers:
                headers[header_name] = ["[REDACTED]"]

        # 2. Sanitize Response Body (OData contexts and SessionIds)
        try:
            import json

            body_str = response["body"]["string"].decode("utf-8")

            # Replace any real hostname occurrences in OData context links
            placeholder_host = "sap-server.example.com"
            body_str = re.sub(
                r"https?://[^/]+/b1s/v\d+",
                f"https://{placeholder_host}/b1s/v2",
                body_str,
            )

            # Redact explicit SessionId in Login responses
            if "SessionId" in body_str:
                data = json.loads(body_str)
                if "SessionId" in data:
                    data["SessionId"] = "REDACTED-SESSION-ID"
                body_str = json.dumps(data)

            response["body"]["string"] = body_str.encode("utf-8")
        except Exception:
            pass

        return response

    return {
        "filter_headers": ["Authorization", "Cookie", "Set-Cookie", "B1SESSION"],
        "before_record_request": before_record_request_cb,
        "before_record_response": before_record_response_cb,
        "decode_compressed_response": True,
        "record_mode": "once",
    }


def pytest_configure(config: Any) -> None:
    """Register custom markers during pytest initialization."""
    config.addinivalue_line(
        "markers",
        "integration: tests that require a real SAP B1 Service Layer connection",
    )
    config.addinivalue_line(
        "markers", "vcr: tests that use pytest-recording to capture HTTP traffic"
    )


@pytest.fixture
def mock_responses() -> Any:
    """Fixture to load mock JSON data from files.

    Returns:
        Callable[[str], Any]: A function that takes a filename (without .json)
        and returns the parsed JSON content.
    """
    import json
    from pathlib import Path

    def _loader(filename: str) -> Any:
        # Resolve path relative to the tests directory
        base_path = Path(__file__).parent / "unit" / "mocks"
        file_path = base_path / f"{filename}.json"

        if not file_path.exists():
            pytest.fail(f"Mock response file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    return _loader
