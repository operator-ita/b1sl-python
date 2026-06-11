"""
b1sl.b1sl.exceptions.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Exception hierarchy for the SAP B1 Service Layer SDK.

All exceptions raised by this SDK are subclasses of ``B1Exception`` so
callers can choose their granularity:

Catch-all::

    except B1Exception as e:
        logger.error(e)

Granular::

    except B1NotFoundError:
        return None            # resource simply doesn't exist
    except B1ValidationError as e:
        raise UserFacingError(str(e)) from e
    except B1AuthError:
        trigger_relogin()
    except SAPConcurrencyError as e:
        # Temporal.io activity: safe to retry after fresh GET
        logger.warning("ETag mismatch on %s", e.endpoint)

HTTP status → exception mapping (applied in ``RestAdapter._do``)
----------------------------------------------------------------
| HTTP status | Exception class        |
|-------------|------------------------|
| 400         | B1ValidationError      |
| 401         | B1AuthError            |
| 404         | B1NotFoundError        |
| 412 + -2039 | SAPConcurrencyError    |
| everything else | B1Exception        |
"""

from __future__ import annotations


class B1Exception(Exception):
    """Base exception for all errors raised by the SAP B1 Service Layer SDK.

    Attributes:
        details: The raw response body (dict) from SAP when available,
                 ``None`` for non-HTTP errors (connection failure, timeout…).
    """

    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(message)
        self.details = details


class B1ConnectionError(B1Exception):
    """Raised when a network-level failure prevents reaching SAP B1.

    Wraps ``httpx.ConnectError``, ``httpx.TimeoutException`` and other
    ``httpx`` network errors (DNS failure, refused connection, read timeout).
    """


class B1PaginationError(B1Exception):
    """Raised when an ``odata.nextLink`` cannot be followed safely.

    Guards against infinite pagination loops: if SAP returns a nextLink whose
    query carries no recognised cursor (``$skip`` / ``$skiptoken``), following
    it would fetch the same page forever.
    """


class B1AuthError(B1Exception):
    """Raised when SAP returns HTTP 401 and the automatic re-login also fails.

    Indicates either invalid credentials or an expired/revoked session that
    could not be refreshed.
    """


class B1NotFoundError(B1Exception):
    """Raised when SAP returns HTTP 404 for a requested resource.

    Callers that treat a missing record as a normal (non-error) case can
    catch this specific subclass::

        try:
            asset = client.assets.get("NONEXISTENT")
        except B1NotFoundError:
            asset = None
    """


class B1ValidationError(B1Exception):
    """Raised when SAP returns HTTP 400 (Bad Request).

    Usually indicates a missing required field, an invalid field value, or
    a business-rule violation on the SAP side.  The ``details`` attribute
    contains the raw SAP error body for inspection.
    """


class B1SqlNotAllowedError(B1ValidationError):
    """Raised when SAP rejects a SQLQuery because a table or column is blocked.

    SAP error codes:
    - ``"702"`` — table not in the server allowlist (``b1s_sqltable.conf``).
    - ``"703"`` — column excluded via ``ColumnExcludeList`` in the same config.

    Neither condition can be fixed at runtime; the SQL text or the server
    configuration must change.  The ``sap_code`` attribute lets callers
    distinguish table-level from column-level blocks::

        try:
            result = client.sql_queries.run("sql04")
        except B1SqlNotAllowedError as e:
            if e.sap_code == "702":
                print(f"Table blocked: {e}")
            else:
                print(f"Column blocked: {e}")
    """

    def __init__(
        self,
        message: str,
        *,
        sap_code: str = "702",
        details: dict | None = None,
    ) -> None:
        super().__init__(message, details=details)
        self.sap_code = sap_code


class B1SqlSyntaxError(B1ValidationError):
    """Raised when SAP rejects a SQL definition or execution due to invalid syntax.

    SAP error code ``"701"`` — covers multiple sub-cases, all requiring a fix
    to the SQL text itself (no runtime adjustment can resolve a 701 error):

    - **Grammar error**: typos like ``ORDER BY x dsc`` instead of ``DESC``.
    - **Unsupported function**: e.g. ``length()``, ``CASE WHEN``, ``COALESCE``.
    - **``SELECT *`` in the top-level query**: only allowed inside subqueries.
    - **Computed column without alias**: ``SUM(col)`` must be aliased as
      ``SUM(col) AS total``.
    - **Duplicate alias**: two columns sharing the same alias are rejected.
    - **DML statement**: ``UPDATE``, ``INSERT``, ``DELETE``, ``ALTER``, etc. —
      the ``SQLQueries`` endpoint accepts only ``SELECT`` queries.

    The SAP error message includes the character position and a description::

        try:
            client.sql_queries.create(en.SQLQuery(sql_code="q1",
                                                   sql_text="select * from ORDR"))
        except B1SqlSyntaxError as e:
            print(e)  # "Invalid SQL syntax: ..., Cannot support asterisk(*)..."
    """

    SAP_ERROR_CODE = "701"

    def __init__(self, message: str, *, details: dict | None = None) -> None:
        super().__init__(message, details=details)
        self.sap_code = self.SAP_ERROR_CODE


class B1SqlParamError(B1ValidationError):
    """Raised when SAP rejects a ``/List`` invocation due to parameter problems.

    SAP error code ``"704"`` — covers missing parameters, extra parameters, or
    type mismatches.  Unlike ``B1SqlNotAllowedError``, this is fixable by the
    caller: check that the kwargs passed to ``run()`` / ``run_stream()`` match
    the ``ParamList`` declared in the stored ``SqlText``::

        try:
            rows = client.sql_queries.run("sql01", doc_total=100)
        except B1SqlParamError:
            # Wrong param name — SAP expects :docTotal, not :doc_total
            rows = client.sql_queries.run("sql01", docTotal=100)

    Note: SAP returns a generic ``"Parameter error."`` message without naming
    the offending parameter.  Inspect the stored query's ``ParamList`` field
    to cross-reference.
    """

    SAP_ERROR_CODE = "704"

    def __init__(
        self,
        message: str,
        *,
        details: dict | None = None,
        expected_params: list[str] | None = None,
    ) -> None:
        super().__init__(message, details=details)
        self.sap_code = self.SAP_ERROR_CODE
        self.expected_params: list[str] | None = expected_params


class B1ResponseError(B1Exception):
    """Raised for unexpected non-2xx responses not covered by other subclasses."""


class SAPConcurrencyError(B1Exception):
    """Raised when SAP returns HTTP 412 Precondition Failed (OData code ``-2039``).

    This indicates that the ETag sent in the ``If-Match`` header no longer
    matches the current server state — another process modified the resource
    since the last GET.

    The correct recovery pattern is:

    1. Re-fetch the resource with a fresh GET (which updates the ETag cache).
    2. Re-apply your business changes on top of the fresh data.
    3. Retry the PATCH / Action.

    Temporal.io usage example::

        from temporalio import activity
        from b1sl.b1sl.exceptions import SAPConcurrencyError

        @activity.defn
        async def update_business_partner(card_code: str, payload: dict) -> None:
            try:
                await adapter.patch(f"/BusinessPartners('{card_code}')", data=payload)
            except SAPConcurrencyError as e:
                # Temporal will retry this activity automatically
                raise ApplicationError(str(e), non_retryable=False) from e

    Attributes:
        sap_code (str): The raw SAP OData error code (typically ``"-2039"``).
        etag_sent (str | None): The ``If-Match`` value that was rejected by SAP.
        endpoint (str): The resource endpoint where the conflict occurred.
        details (dict | None): Full SAP error body for detailed inspection.
    """

    SAP_ERROR_CODE = "-2039"

    def __init__(
        self,
        message: str,
        *,
        sap_code: str = "-2039",
        etag_sent: str | None = None,
        endpoint: str = "",
        details: dict | None = None,
    ) -> None:
        super().__init__(message, details=details)
        self.sap_code = sap_code
        self.etag_sent = etag_sent
        self.endpoint = endpoint
