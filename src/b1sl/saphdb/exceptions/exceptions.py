class SapHAClientException(Exception):
    """Base exception for all SAP HANA client errors."""

    def __init__(self, message, details=None):
        super().__init__(message)
        self.details = details


class SapHAClientConnectionError(SapHAClientException):
    pass


class SapHAClientResponseError(SapHAClientException):
    pass


# Legacy aliases
B1ClientConnectionError = SapHAClientConnectionError
B1ClientResponseError = SapHAClientResponseError
