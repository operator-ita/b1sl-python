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

    Wraps ``requests.exceptions.ConnectionError`` and
    ``requests.exceptions.Timeout``.
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
