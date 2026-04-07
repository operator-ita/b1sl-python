from typing import Optional

from b1sl.saphdb.config import SapHDBConfig
from b1sl.saphdb.odbc_adapter import HDBCliAdapter

# This module provides a shared odbc_adapter instance for Django users.
# It uses settings.SAPODBCLIENT_* vars from the Django environment.
# Avoid importing this if not in a Django context.

_odbc_adapter: Optional[HDBCliAdapter] = None


def get_odbc_adapter() -> HDBCliAdapter:
    global _odbc_adapter
    if _odbc_adapter is None:
        _odbc_adapter = HDBCliAdapter.from_config(SapHDBConfig.from_django_settings())
    return _odbc_adapter


# Legacy support for direct access
try:
    odbc_adapter = get_odbc_adapter()
except Exception:
    odbc_adapter = None
