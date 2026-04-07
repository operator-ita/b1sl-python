"""
b1sl.b1sl.models — public model re-exports.

    from b1sl.b1sl.models import B1Model, PaginatedResult
"""

from b1sl.b1sl.models.base import B1Model
from b1sl.b1sl.models.paginated_result import PaginatedResult

__all__ = [
    "B1Model",
    "PaginatedResult",
]
