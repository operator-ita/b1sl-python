from .base import SapMiddlewareBase


class ODataTransformURLMiddleware(SapMiddlewareBase):
    """Transforms OData-style URLs (replacing parenthesis) before Django routing."""

    def process_request(self, request):
        path = request.path
        if "(" in path and ")" in path:
            # Reemplazar '(' y ')' con '/'
            request.path = path.replace("(", "/").replace(")", "")
            print(request.path)

    async def async_process_request(self, request):
        self.process_request(request)  # pure string op, no I/O
