import pytest

from b1sl.saphdb.config import SapHDBConfig
from b1sl.saphdb.odbc_adapter import HDBCliAdapter


def test_saphdb_config_from_env_missing():
    with pytest.MonkeyPatch.context() as m:
        m.delenv("SAPODBCLIENT_ADDRESS", raising=False)
        with pytest.raises(EnvironmentError):
            SapHDBConfig.from_env()


def test_saphdb_config_from_env_success():
    with pytest.MonkeyPatch.context() as m:
        m.setenv("SAPODBCLIENT_ADDRESS", "localhost")
        m.setenv("SAPODBCLIENT_PORT", "30015")
        m.setenv("SAPODBCLIENT_USER", "SYSTEM")
        m.setenv("SAPODBCLIENT_PASSWORD", "secret")
        m.setenv("SAPODBCLIENT_COMPANY_DB", "HDB")

        config = SapHDBConfig.from_env()

        assert config.address == "localhost"
        assert config.port == 30015
        assert config.schema == "HDB"


def test_saphdb_adapter_from_config():
    config = SapHDBConfig(
        address="10.0.0.1", port=30015, user="sys", password="p", schema="sys_schema"
    )

    # Clear singleton instance for testing
    HDBCliAdapter._instance = None
    adapter = HDBCliAdapter.from_config(config)

    assert adapter.address == "10.0.0.1"
    assert adapter.port == 30015
    assert adapter.schema == "sys_schema"
