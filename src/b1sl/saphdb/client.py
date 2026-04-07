"""
SapHDBClient — Framework-agnostic entry point for SAP HANA ODBC SDK.

Usage (standalone / scripts):
    from b1sl.saphdb import SapHDBClient, SapHDBConfig
    config = SapHDBConfig.from_env()
    client = SapHDBClient(config)

Usage (Django — in service layer only):
    from b1sl.saphdb import SapHDBClient, SapHDBConfig
    config = SapHDBConfig.from_django_settings()
    client = SapHDBClient(config)
"""

from __future__ import annotations

import logging

from b1sl.saphdb.config import SapHDBConfig
from b1sl.saphdb.odbc_adapter import HDBCliAdapter


class SapHDBClient:
    """
    Public interface for the SAP HANA ODBC SDK.
    """

    def __init__(
        self,
        config: SapHDBConfig,
        logger: logging.Logger | None = None,
    ) -> None:
        self._logger = logger or logging.getLogger(__name__)
        self._adapter = HDBCliAdapter.from_config(config, logger=self._logger)

        # Lazy resources
        self._serial_numbers = None

    @property
    def serial_numbers(self):
        """Access the SerialNumberDetails ODBC resource."""
        if self._serial_numbers is None:
            from b1sl.saphdb.endpoints.serialnumberdetailodbc import (
                SerialNumberDetailsODBCEndpoint,
            )

            self._serial_numbers = SerialNumberDetailsODBCEndpoint(
                adapter=self._adapter
            )
        return self._serial_numbers
