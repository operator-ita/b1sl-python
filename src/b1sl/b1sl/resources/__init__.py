"""
b1sl.b1sl.resources — public resource re-exports.
"""

from b1sl.b1sl.resources.base import GenericResource
from b1sl.b1sl.resources.udo import UDOResource

__all__ = [
    "GenericResource",
    "UDOResource",
]
