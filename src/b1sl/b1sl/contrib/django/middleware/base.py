"""
b1sl.b1sl.contrib.django.middleware.base
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Framework-agnostic base class for all SAP-aware Django middleware.
Supports both WSGI (__call__) and ASGI (__acall__) deployments.
"""

from __future__ import annotations

import logging
from typing import Callable

logger = logging.getLogger(__name__)


class SapMiddlewareBase:
    """
    Drop-in Django middleware base that works with both:
      - WSGI: Django calls __call__(request) synchronously.
      - ASGI: Django calls __call__(scope, receive, send) or uses
              the middleware with channels / uvicorn via __acall__.

    Subclass and override `process_request` / `process_response`
    for custom logic.
    """

    sync_capable = True
    async_capable = True

    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response
        # Detect if the downstream handler is async
        import asyncio

        self._is_coroutine = asyncio.iscoroutinefunction(self.get_response)

    # ------------------------------------------------------------------ #
    # Hooks — override in subclasses                                       #
    # ------------------------------------------------------------------ #

    def process_request(self, request):
        """Synchronous pre-processing hook. Return None to continue."""

    def process_response(self, request, response):
        """Synchronous post-processing hook. Must return response."""
        return response

    async def async_process_request(self, request):
        """Async pre-processing hook. Return None to continue."""

    async def async_process_response(self, request, response):
        """Async post-processing hook. Must return response."""
        return response

    # ------------------------------------------------------------------ #
    # WSGI path                                                            #
    # ------------------------------------------------------------------ #

    def __call__(self, request):
        if self._is_coroutine:
            # Do not call this synchronously on an async handler —
            # Django will always use __acall__ in that case.
            import asyncio

            return asyncio.get_event_loop().run_until_complete(self.__acall__(request))

        short_circuit = self.process_request(request)
        if short_circuit is not None:
            return short_circuit

        response = self.get_response(request)

        return self.process_response(request, response)

    # ------------------------------------------------------------------ #
    # ASGI path                                                            #
    # ------------------------------------------------------------------ #

    async def __acall__(self, request):
        short_circuit = await self.async_process_request(request)
        if short_circuit is not None:
            return short_circuit

        if self._is_coroutine:
            response = await self.get_response(request)
        else:
            response = self.get_response(request)

        return await self.async_process_response(request, response)
