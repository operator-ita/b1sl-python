"""Security posture of B1Config: no password in repr, TLS warning on disable."""
import logging

import pytest

from b1sl.b1sl.config import B1Config


@pytest.fixture
def config():
    return B1Config(
        base_url="https://sap-host:50000",
        username="manager",
        password="SuperSecret!",
        company_db="SBODEMO",
    )


def test_repr_does_not_leak_password(config):
    assert "SuperSecret!" not in repr(config)
    assert "SuperSecret!" not in str(config)


def test_password_still_accessible(config):
    # repr masking must not break programmatic access
    assert config.password == "SuperSecret!"


def test_disabled_tls_emits_warning(config, caplog):
    from b1sl.b1sl.rest_adapter import RestAdapter

    insecure = B1Config(
        base_url="https://sap-host:50000",
        username="manager",
        password="x",
        company_db="SBODEMO",
        ssl_verify=False,
    )
    with caplog.at_level(logging.WARNING, logger="b1sl"):
        RestAdapter(insecure)
    assert any("TLS certificate verification is DISABLED" in r.message for r in caplog.records)


def test_enabled_tls_emits_no_warning(config, caplog):
    from b1sl.b1sl.rest_adapter import RestAdapter

    with caplog.at_level(logging.WARNING, logger="b1sl"):
        RestAdapter(config)
    assert not any("TLS certificate verification" in r.message for r in caplog.records)
