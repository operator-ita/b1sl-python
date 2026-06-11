"""
b1sl — async-first Python SDK for the SAP Business One Service Layer.

The implementation lives in the ``b1sl.b1sl`` subpackage; this top-level
package lazily re-exports the public surface so that the natural import
works out of the box::

    from b1sl import AsyncB1Client, B1Config, entities

Lazy forwarding (PEP 562) keeps ``import b1sl`` itself instant — nothing is
loaded until the first attribute access.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("b1sl-python")
except PackageNotFoundError:  # source checkout without an installed distribution
    __version__ = "0.0.0+unknown"

# Public names forwarded from b1sl.b1sl on first access.
_FORWARDED = (
    "B1Client",
    "AsyncB1Client",
    "B1Config",
    "B1Environment",
    "B1Env",
    "PaginatedResult",
    "entities",
    "fields",
)

__all__ = ["__version__", *_FORWARDED]


def __getattr__(name: str):
    if name in _FORWARDED:
        from b1sl import b1sl as _impl

        return getattr(_impl, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(__all__)
