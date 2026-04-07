"""
b1sl.b1sl.contrib.django.middleware.odata_decode_middleware
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
URL-decodes percent-encoded OData query strings before Django routing.
"""

from urllib.parse import unquote

from b1sl.b1sl.contrib.django.middleware.base import SapMiddlewareBase


class ODataDecodeMiddleware(SapMiddlewareBase):
    """URL-decodes percent-encoded OData query strings before Django routing."""

    def process_request(self, request):
        if qs := request.META.get("QUERY_STRING"):
            request.META["QUERY_STRING"] = unquote(qs)

    async def async_process_request(self, request):
        self.process_request(request)  # pure string op, no I/O
