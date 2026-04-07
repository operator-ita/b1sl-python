import urllib.parse
from unittest.mock import MagicMock

from b1sl.contrib.django import ODataDecodeMiddleware, ODataTransformURLMiddleware


class DummyRequest:
    def __init__(self, path="/", meta=None):
        self.path = path
        self.META = meta or {}


def dummy_get_response(request):
    return MagicMock(status_code=200)


def test_odata_decode_middleware():
    mw_instance = ODataDecodeMiddleware(dummy_get_response)

    # Original query string encoded
    original_qs = "param=" + urllib.parse.quote("a values(1)")
    request = DummyRequest(meta={"QUERY_STRING": original_qs})

    mw_instance.process_request(request)

    # Check that it got decoded
    assert request.META["QUERY_STRING"] == "param=a values(1)"


def test_odata_transform_url_middleware():
    mw_instance = ODataTransformURLMiddleware(dummy_get_response)

    request = DummyRequest(path="/api/Resources('123')/data")
    mw_instance.process_request(request)

    # Check that parenthesis replaced by slashes and removed
    assert request.path == "/api/Resources/'123'/data"
