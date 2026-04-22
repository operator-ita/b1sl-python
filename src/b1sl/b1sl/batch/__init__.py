"""OData $batch support for the b1sl SDK."""

from .client import BatchClient
from .results import BatchResult, BatchResults

__all__ = ["BatchClient", "BatchResult", "BatchResults"]
