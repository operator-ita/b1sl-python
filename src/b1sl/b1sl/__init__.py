"""
b1sl.b1sl — SDK for SAP B1 Service Layer (OData).
"""

import logging
import warnings

from b1sl.b1sl.async_client import AsyncB1Client
from b1sl.b1sl.async_rest_adapter import AsyncRestAdapter
from b1sl.b1sl.base_adapter import HookContext, ObservabilityConfig
from b1sl.b1sl.client import B1Client
from b1sl.b1sl.config import B1Config
from b1sl.b1sl.config_manager import B1Environment
from b1sl.b1sl.environment import B1Env
from b1sl.b1sl.exceptions.exceptions import SAPConcurrencyError
from b1sl.b1sl.resources.async_base import AsyncGenericResource
from b1sl.b1sl.resources.base import GenericResource, ODataQuery
from b1sl.b1sl.rest_adapter import RestAdapter

try:
    from pydantic import ArbitraryTypeWarning

    warnings.filterwarnings("ignore", category=ArbitraryTypeWarning, module=r"b1sl\..*")  # type: ignore
except ImportError:
    warnings.filterwarnings("ignore", module=r"b1sl\..*|pydantic\..*")

# Standard library pattern: prevent "No handlers could be found"
logging.getLogger("b1sl").addHandler(logging.NullHandler())

try:
    from b1sl.b1sl import entities  # type: ignore
except ImportError:
    entities = None  # type: ignore # Before code generation

try:
    from b1sl.b1sl import fields  # type: ignore
except ImportError:
    fields = None  # type: ignore

__all__ = [
    "AsyncB1Client",
    "B1Client",
    "B1Config",
    "B1Environment",
    "AsyncRestAdapter",
    "RestAdapter",
    "B1Env",
    "SAPConcurrencyError",
    "AsyncGenericResource",
    "GenericResource",
    "ODataQuery",
    "entities",
    "fields",
    "HookContext",
    "ObservabilityConfig",
]
