"""Hand-written extensions of generated entity models.

This package survives metadata regeneration — `_generated/` does not.
To extend an entity, define a class with the SAME name in a module here,
subclassing the generated model:

    # _overrides/inventory.py
    from .._generated.entities.inventory import Item as _Item

    class Item(_Item):
        @property
        def available_stock(self) -> float: ...

Discovery is dynamic: the entities facade scans this package on first
entity access and serves your subclass everywhere (``en.Item``, nested
validation, resource deserialization). No registration or regeneration
is needed for runtime behavior; re-running ``generate_models.sh`` only
refreshes the facade's TYPE_CHECKING imports so IDEs resolve the
override type. See docs/07-overrides-and-udfs.md.
"""
