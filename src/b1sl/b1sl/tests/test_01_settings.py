"""
test_01_config.py — B1Config unit tests (pure pytest, no Django).

Renamed from test_01_settings.py which required Django settings.
"""

from datetime import timedelta

import pytest

from b1sl.b1sl.config import B1Config


def test_config_rejects_empty_base_url():
    with pytest.raises(ValueError, match="base_url"):
        B1Config(base_url="", username="u", password="p", company_db="db")


def test_config_rejects_empty_credentials():
    with pytest.raises(ValueError, match="credentials"):
        B1Config(base_url="https://x", username="", password="", company_db="db")


def test_config_rejects_empty_company_db():
    with pytest.raises(ValueError, match="company_db"):
        B1Config(base_url="https://x", username="u", password="p", company_db="")


def test_config_defaults():
    cfg = B1Config(base_url="https://x", username="u", password="p", company_db="db")
    assert cfg.ssl_verify is True
    assert cfg.reuse_token is True
    assert cfg.token_timeout == timedelta(seconds=900)
    assert cfg.max_page_size == 20
    assert cfg.connect_timeout == 10.0
    assert cfg.read_timeout == 60.0


def test_config_from_env_success():
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv("SAPB1CLIENT_BASE_URL", "https://sap:50000/b1s/v1")
        mp.setenv("SAPB1CLIENT_USERNAME", "admin")
        mp.setenv("SAPB1CLIENT_PASSWORD", "pass")
        mp.setenv("SAPB1CLIENT_COMPANY_DB", "MYDB")
        cfg = B1Config.from_env()
    assert cfg.base_url == "https://sap:50000/b1s/v1"
    assert cfg.company_db == "MYDB"


def test_config_from_env_missing_raises():
    with pytest.MonkeyPatch.context() as mp:
        for key in (
            "SAPB1CLIENT_BASE_URL",
            "SAPB1CLIENT_USERNAME",
            "SAPB1CLIENT_PASSWORD",
            "SAPB1CLIENT_COMPANY_DB",
        ):
            mp.delenv(key, raising=False)
        with pytest.raises(EnvironmentError):
            B1Config.from_env()
