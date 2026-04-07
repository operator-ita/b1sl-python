"""
b1sl.b1sl.contrib.django.middleware.odata_transform_url_middleware
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Transforms OData-style URLs (replacing parentheses) before Django routing.
"""

from b1sl.b1sl.contrib.django.middleware.base import SapMiddlewareBase


class ODataTransformURLMiddleware(SapMiddlewareBase):
    """Transforms OData-style URLs (replacing parenthesis) before Django routing."""

    def process_request(self, request):
        path = request.path
        if "(" in path and ")" in path:
            # Replace '(' and ')' with '/'
            request.path = path.replace("(", "/").replace(")", "")

    async def async_process_request(self, request):
        self.process_request(request)  # pure string op, no I/O
