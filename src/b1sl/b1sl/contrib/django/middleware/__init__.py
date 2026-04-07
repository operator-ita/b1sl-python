"""
b1sl.b1sl.contrib.django.middleware
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Django middleware classes for SAP B1 Service Layer integration.

Add to Django's MIDDLEWARE list::

    MIDDLEWARE = [
        ...
        "b1sl.b1sl.contrib.django.middleware.odata_decode_middleware.ODataDecodeMiddleware",
        # "b1sl.b1sl.contrib.django.middleware.odata_transform_url_middleware.ODataTransformURLMiddleware",
    ]
"""

from b1sl.b1sl.contrib.django.middleware.base import SapMiddlewareBase
from b1sl.b1sl.contrib.django.middleware.odata_decode_middleware import (
    ODataDecodeMiddleware,
)
from b1sl.b1sl.contrib.django.middleware.odata_transform_url_middleware import (
    ODataTransformURLMiddleware,
)

__all__ = [
    "SapMiddlewareBase",
    "ODataDecodeMiddleware",
    "ODataTransformURLMiddleware",
]
