import os
import re
from typing import Any
from urllib.parse import urlsplit

import pytest

from b1sl.b1sl.client import B1Client
from b1sl.b1sl.config import B1Config
from tests.fakes.fake_rest_adapter import FakeRestAdapter

# Load common test fixtures
pytest_plugins = ["tests.fixtures.test_data"]


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


def _real_hosts() -> list[str]:
    """Hosts that must never appear in cassettes.

    During recording the real SAP host is known via B1SL_BASE_URL; collect
    both ``host:port`` and bare ``host`` so any occurrence (URIs, OData
    context links, error messages) can be rewritten.
    """
    hosts: list[str] = []
    base = os.environ.get("B1SL_BASE_URL", "")
    if base:
        parts = urlsplit(base)
        if parts.netloc:
            hosts.append(parts.netloc)
        if parts.hostname and parts.hostname != parts.netloc:
            hosts.append(parts.hostname)
    return hosts


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

                # Define keys to redact (a prod re-record must not leak the
                # real username either)
                to_redact = {"password", "companydb", "company_db", "username"}
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
            body_str = response["body"]["string"].decode("utf-8")

            placeholder_host = "sap-server.example.com"

            # Rewrite the real recording host anywhere in the body (not only
            # in /b1s/ context links — error messages and metadata URLs too)
            for host in _real_hosts():
                body_str = body_str.replace(host, placeholder_host)

            # Belt-and-braces: any host followed by a /b1s/ path
            body_str = re.sub(
                r"https?://[^/]+/b1s/v\d+",
                f"https://{placeholder_host}/b1s/v2",
                body_str,
            )

            # Redact SessionId at ANY nesting depth (regex, not top-level dict)
            body_str = re.sub(
                r'"SessionId"\s*:\s*"[^"]*"',
                '"SessionId": "REDACTED-SESSION-ID"',
                body_str,
            )
            # Redact raw B1SESSION cookie values echoed in bodies
            body_str = re.sub(
                r"B1SESSION=[^;\"'\s]+", "B1SESSION=REDACTED", body_str
            )

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
