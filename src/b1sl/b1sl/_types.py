"""
b1sl.b1sl._types
~~~~~~~~~~~~~~~~~~~~~~
Shared generic type variables for the SDK.

Import ``T`` from here instead of re-declaring it per-module so that
static analysis tools (mypy, pyright) resolve the same TypeVar object
across resource classes and the public API.

Usage::

    from b1sl.b1sl._types import T

    def get(self, code: str, *, model: Type[T] | None = None) -> MyModel | T:
        ...
"""

from __future__ import annotations

from typing import TypeVar

from pydantic import BaseModel

# T represents *any* Pydantic model a downstream developer injects.
# Bound to BaseModel so IDEs know every T has .model_validate(), .model_dump(), etc.
T = TypeVar("T", bound=BaseModel)

__all__ = ["T"]
