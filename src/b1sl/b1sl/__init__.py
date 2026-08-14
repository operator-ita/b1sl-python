"""
b1sl.b1sl — SDK for SAP B1 Service Layer (OData).
"""

import logging
from typing import TYPE_CHECKING, Any

from b1sl.b1sl.async_client import AsyncB1Client
from b1sl.b1sl.async_rest_adapter import AsyncRestAdapter
from b1sl.b1sl.base_adapter import HookContext, ObservabilityConfig
from b1sl.b1sl.client import B1Client
from b1sl.b1sl.config import B1Config
from b1sl.b1sl.config_manager import B1Environment
from b1sl.b1sl.environment import B1Env
from b1sl.b1sl.exceptions.exceptions import (
    B1ConnectionError,
    B1PaginationError,
    B1SqlNotAllowedError,
    B1SqlParamError,
    B1SqlSyntaxError,
    SAPConcurrencyError,
)
from b1sl.b1sl.models.multipart import MultipartFile
from b1sl.b1sl.models.paginated_result import PaginatedResult
from b1sl.b1sl.resources.async_base import AsyncGenericResource
from b1sl.b1sl.resources.base import GenericResource, ODataQuery
from b1sl.b1sl.resources.sql_queries import (
    DEFAULT_ACCESSIBLE_TABLES,
    KNOWN_INACCESSIBLE_PATTERNS,
    SQLQueryInfo,
    SQLRunResult,
)
from b1sl.b1sl.rest_adapter import RestAdapter

try:
    from b1sl.b1sl import fields  # type: ignore
except ImportError:
    fields = None  # type: ignore

if TYPE_CHECKING:
    # Static analysers / IDEs still resolve ``b1sl.b1sl.entities`` even though it
    # is loaded lazily at runtime (see ``__getattr__`` below).
    from b1sl.b1sl import entities


def __getattr__(name: str) -> Any:
    """PEP 562 lazy attribute access.

    ``entities`` blends ~280 SAP models. Deferring the module import keeps
    ``from b1sl.b1sl import B1Client`` fast, and the facade itself is also lazy:
    each model's Pydantic core-schema is compiled on first attribute access
    (``en.Item``), never for the whole graph at once — building all ~280 schemas
    eagerly used to cost ~14s and ~2.4 GiB RSS. Call ``entities.preload()`` to
    opt into eager warm-up at startup.
    """
    if name == "entities":
        import importlib

        # ``import_module`` loads the submodule directly via sys.modules instead of
        # the ``from b1sl.b1sl import entities`` form, whose fromlist machinery would
        # re-enter this ``__getattr__`` and recurse infinitely.
        return importlib.import_module("b1sl.b1sl.entities")
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

# Standard library pattern: prevent "No handlers could be found"
logging.getLogger("b1sl").addHandler(logging.NullHandler())

__all__ = [
    "AsyncB1Client",
    "B1Client",
    "B1Config",
    "B1Environment",
    "AsyncRestAdapter",
    "RestAdapter",
    "B1Env",
    "SAPConcurrencyError",
    "B1ConnectionError",
    "B1PaginationError",
    "B1SqlSyntaxError",
    "B1SqlNotAllowedError",
    "B1SqlParamError",
    "AsyncGenericResource",
    "GenericResource",
    "ODataQuery",
    "PaginatedResult",
    "MultipartFile",
    "DEFAULT_ACCESSIBLE_TABLES",
    "KNOWN_INACCESSIBLE_PATTERNS",
    "SQLQueryInfo",
    "SQLRunResult",
    "entities",
    "fields",
    "HookContext",
    "ObservabilityConfig",
]
