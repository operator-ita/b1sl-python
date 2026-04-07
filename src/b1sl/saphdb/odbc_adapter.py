import logging
import threading
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from hdbcli import dbapi
from pydantic import BaseModel

from b1sl.saphdb.models.result import Result


class QueryResult(BaseModel):
    data: List[Dict[str, Any]]


class HDBCliAdapter:
    @classmethod
    def from_config(
        cls, config, logger: Optional[logging.Logger] = None
    ) -> "HDBCliAdapter":
        return cls(
            address=config.address,
            port=config.port,
            user=config.user,
            password=config.password,
            schema=config.schema,
            logger=logger,
            reuse_connection=config.reuse_connection,
            connection_timeout=config.connection_timeout,
        )

    def __init__(
        self,
        address: str,
        port: int,
        user: str,
        password: str,
        schema: str,
        logger: Optional[logging.Logger] = None,
        reuse_connection: bool = False,
        connection_timeout: timedelta = timedelta(seconds=900),
    ):
        self._lock = threading.RLock()
        self.address = address
        self.port = port
        self.user = user
        self.password = password
        self.schema = schema
        self.logger = logger or logging.getLogger(__name__)

        self.connection = None
        self.reuse_connection = reuse_connection
        self.connection_timeout = connection_timeout
        self.connection_expiry = None

    def connect(self):
        """Idempotent and thread-safe connection establishment with liveness check."""
        with self._lock:
            if self.connection is None or self._is_connection_expired():
                # Close the dead socket gracefully if possible
                if self.connection is not None:
                    try:
                        self.connection.close()
                    except Exception:
                        pass
                    finally:
                        self.connection = None

                try:
                    self.connection = dbapi.connect(
                        address=self.address,
                        port=self.port,
                        user=self.user,
                        password=self.password,
                    )
                    self.connection_expiry = datetime.now() + self.connection_timeout
                    self.logger.info("Connected to HANA database")
                except dbapi.Error as e:
                    self.logger.error(
                        f"Failed to connect to HANA database: {e.errortext} (Code: {e.errorcode})"
                    )
                    raise
                except Exception as e:
                    self.logger.error(
                        f"Failed to connect to HANA (Network/OS Error): {e}"
                    )
                    raise

    def _is_connection_expired(self) -> bool:
        """Checks both clock-based timeout and actual socket liveness."""
        if self.connection_expiry is None or self.connection is None:
            return True
        if datetime.now() >= self.connection_expiry:
            return True

        # Real Liveness Check (hdbcli specific)
        try:
            if hasattr(self.connection, "isconnected"):
                if not self.connection.isconnected():
                    self.logger.warning("HANA socket is natively reported as dead.")
                    return True
            else:
                # Fallback if driver version lacks isconnected(): ping via dummy execute
                cursor = self.connection.cursor()
                cursor.execute("SELECT 1 FROM DUMMY")
                cursor.close()
        except dbapi.Error:
            self.logger.warning("HANA socket is dead (failed liveness ping).")
            return True
        return False

    @contextmanager
    def transaction(self):
        """
        Transactional Context Manager.
        Ensures atomic execution: COMMIT on success, ROLLBACK on error.
        """
        with self._lock:
            self.connect()
            try:
                yield self.connection
                self.connection.commit()
                self.logger.debug("Transaction committed.")
            except dbapi.Error as e:
                try:
                    self.connection.rollback()
                except Exception:
                    pass
                self.logger.error(
                    f"Transaction rolled back due to HANA error: {e.errortext} (Code: {e.errorcode})"
                )
                raise
            except Exception as e:
                try:
                    self.connection.rollback()
                except Exception:
                    pass
                self.logger.error(f"Transaction rolled back due to Runtime Error: {e}")
                raise

    def execute_query(
        self,
        query: str,
        params: Optional[Tuple[Any, ...]] = None,
        schema: Optional[str] = None,
    ) -> Result:
        """
        Executes a query safely using bind variables.
        """
        with self._lock:
            cursor = None
            try:
                # Use transactional scope for query execution
                with self.transaction() as conn:
                    cursor = conn.cursor()

                    # Sanitize schema name (SQL injection prevention for identifiers)
                    active_schema = schema or self.schema
                    if active_schema:
                        # Add double quotes to prevent identifier injection
                        cursor.execute(f'SET SCHEMA "{active_schema}"')
                        self.logger.debug(f"Schema set to: {active_schema}")

                    # Execute safely with bind variables
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)

                    self.logger.info("Query executed successfully.")

                    if cursor.description:
                        columns = [col[0] for col in cursor.description]
                        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
                    else:
                        results = []

                    return Result(
                        status_code=200,
                        message="Query executed successfully.",
                        data=results,
                    )
            except dbapi.Error as e:
                self.logger.error(
                    f"HANA Query error: {e.errortext} (Code: {e.errorcode})"
                )
                return Result(
                    status_code=500,
                    message=f"SAP HANA Error [{e.errorcode}]: {e.errortext}",
                )
            except Exception as e:
                self.logger.error(f"Runtime query execution error: {e}")
                return Result(status_code=500, message=f"Runtime query error: {str(e)}")
            finally:
                if cursor:
                    cursor.close()
                if not self.reuse_connection:
                    self.close()

    def close(self):
        """Idempotent closure of resources."""
        with self._lock:
            if self.connection is not None:
                try:
                    self.connection.close()
                except Exception:
                    pass
                finally:
                    self.connection = None
                    self.connection_expiry = None
                    self.logger.info("Connection closed.")

    # Support for simple 'with adapter:' usage
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
