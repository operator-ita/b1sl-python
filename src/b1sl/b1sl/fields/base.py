from __future__ import annotations

from b1sl.b1sl.resources.odata import ODataField

__all__ = ["FieldMeta", "FieldEnum", "ODataField"]


class FieldMeta(type):
    """
    Metaclass that makes field containers iterable and 
    allows discovery of fields.
    """
    def __iter__(cls):
        # Return all public attributes (fields)
        # We filter out _ and keep only those that were explicitly defined
        return (getattr(cls, name) for name in dir(cls) if not name.startswith("_") and not callable(getattr(cls, name)))

class FieldEnum(metaclass=FieldMeta):
    """
    Base class for generated field constants.
    Replaces StrEnum to allow operator overloading while maintaining 
    string behavior and iterability.
    """
    pass
