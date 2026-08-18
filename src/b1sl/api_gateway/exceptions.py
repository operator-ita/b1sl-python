"""
b1sl.api_gateway.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Exception hierarchy for the SAP B1 **API Gateway** client.

The API Gateway is a separate service from the Service Layer (different
port, path, session cookie and authorization). Failures must be
distinguishable from Service Layer failures, so every exception raised by
:mod:`b1sl.api_gateway` derives from :class:`APIGatewayError`.

Where the semantics match a Service Layer exception the gateway class also
inherits from it (``APIGatewayConnectionError`` *is a* ``B1ConnectionError``),
so a broad ``except B1ConnectionError`` still works — but
``except APIGatewayError`` isolates the gateway boundary.

The gateway does **not** signal failures with HTTP status codes in several
cases (see ``docs/20-api-gateway.md``). The specialised subclasses below
map those body-level signals to typed errors:

| Signal                                    | Exception                        |
|-------------------------------------------|----------------------------------|
| network failure / timeout                 | APIGatewayConnectionError        |
| login rejected / session cannot be renewed| APIGatewayAuthError              |
| ``LoadCR`` answers ``{}``                 | APIGatewayLayoutNotFoundError    |
| ``ExportPDFData`` answers ``(---)``       | APIGatewayParameterError         |
| decoded body is not ``%PDF-``             | APIGatewayPDFError               |
| any other unexpected response             | APIGatewayResponseError          |
"""

from __future__ import annotations

from b1sl.b1sl.exceptions.exceptions import (
    B1AuthError,
    B1ConnectionError,
    B1Exception,
)


class APIGatewayError(B1Exception):
    """Base class for every error raised by the API Gateway client.

    Attributes:
        details: Raw response body (parsed JSON when possible, otherwise the
            decoded text) or ``None`` for non-HTTP failures.
    """


class APIGatewayConnectionError(APIGatewayError, B1ConnectionError):
    """The API Gateway host could not be reached (DNS, refused, timeout…).

    Note the gateway listens on its own port (``60000`` by default) — a
    healthy Service Layer says nothing about the gateway being up.
    """


class APIGatewayAuthError(APIGatewayError, B1AuthError):
    """``/login`` was rejected, or the session expired and re-login failed.

    Besides bad credentials, the SAP user needs the *Report Layout API*
    general authorization for the gateway to accept the login.
    """


class APIGatewayResponseError(APIGatewayError):
    """The gateway answered with an unexpected status or body shape."""


class APIGatewayLayoutNotFoundError(APIGatewayError):
    """``LoadCR`` returned an empty body: the ``DocCode`` does not exist.

    The gateway signals a missing layout with ``200 OK`` and ``{}``, not
    with a 404. Typically means the layout was deleted/renumbered in SAP and
    a hard-coded ``DocCode`` mapping is stale.
    """

    def __init__(self, doc_code: str, details: dict | None = None) -> None:
        super().__init__(
            f"Layout '{doc_code}' does not exist in SAP (LoadCR returned an "
            "empty result).",
            details=details,
        )
        self.doc_code = doc_code


class APIGatewayParameterError(APIGatewayError):
    """``ExportPDFData`` declined to render — answered ``(---)``.

    The gateway signals *any* render failure with ``200 OK`` and the literal
    5-byte body ``(---)``: malformed payload, an included empty optional
    parameter, an unparseable value, an unknown ``DocCode``, or a transient
    collision between concurrent exports on one session (the clients retry
    once before raising). Also raised locally when a required parameter has
    no value and none was supplied.
    """


class APIGatewayPDFError(APIGatewayResponseError):
    """``ExportPDFData`` succeeded but the decoded body is not a PDF.

    The client checks the ``%PDF-`` magic bytes before returning bytes so a
    corrupt/HTML/error body is never handed back as a document.
    """
