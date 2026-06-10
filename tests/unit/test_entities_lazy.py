"""Lazy entity-schema compilation in the ``entities`` facade.

The facade resolves entity classes via PEP 562 ``__getattr__`` and builds each
pydantic core schema on first access. Building the full graph eagerly costs
~13s / ~2.4 GiB RSS, which made the SDK unusable in memory-constrained pods.

These tests run in subprocesses: laziness can only be observed in a fresh
interpreter, since any other test touching ``entities`` would already have
built some models in this process.
"""

import subprocess
import sys
import textwrap

import pytest


def run_py(code: str) -> str:
    result = subprocess.run(
        [sys.executable, "-c", textwrap.dedent(code)],
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout


@pytest.mark.parametrize("variant", ["module_getattr", "from_import"])
def test_access_builds_only_the_closure(variant):
    """Touching one entity must not compile the rest of the graph."""
    access = {
        "module_getattr": "item_cls = en.Item",
        "from_import": "from b1sl.b1sl.entities import Item as item_cls",
    }[variant]
    out = run_py(f"""
        from b1sl.b1sl import entities as en
        from b1sl.b1sl.models._generated import entities as gen

        untouched = gen._NAMESPACE["JournalEntry"]
        print("untouched before:", untouched.__pydantic_complete__)

        {access}
        instance = item_cls(item_code="A001", item_name="Widget")
        print("payload:", instance.to_api_payload())
        print("untouched after:", untouched.__pydantic_complete__)
    """)
    assert "untouched before: False" in out
    assert "payload: {'ItemCode': 'A001', 'ItemName': 'Widget'}" in out
    assert "untouched after: False" in out


def test_aliases_resolve_to_canonical_models():
    out = run_py("""
        from b1sl.b1sl import entities as en
        print("alias is canonical:", en.Order is en.Document)
        order = en.Order(card_code="C001")
        print("payload:", order.to_api_payload())
    """)
    assert "alias is canonical: True" in out
    assert "payload: {'CardCode': 'C001'}" in out


def test_overrides_are_blended():
    out = run_py("""
        # Importing the override module FIRST is the regression case: overrides
        # used to be imported by the generated package at init time, so this
        # exact order raised ImportError (circular import). Overrides are now
        # blended lazily via _apply_overrides() on first entity access.
        from b1sl.b1sl.models._overrides.inventory import Item as Override

        from b1sl.b1sl import entities as en
        print("facade serves override:", en.Item is Override)
        print("has property:", hasattr(en.Item(item_code="X"), "available_stock"))
    """)
    assert "facade serves override: True" in out
    assert "has property: True" in out


def test_unknown_attribute_raises():
    out = run_py("""
        from b1sl.b1sl import entities as en
        try:
            en.NotAnEntity
        except AttributeError as exc:
            print("raised:", exc)
        print("dir has entities:", "Quotation" in dir(en) and "Item" in dir(en))
    """)
    assert "raised:" in out
    assert "NotAnEntity" in out
    assert "dir has entities: True" in out


def test_concurrent_first_access_is_safe():
    out = run_py("""
        import threading
        from b1sl.b1sl import entities as en

        errors = []

        def build():
            try:
                en.JournalEntry(memo="x")
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=build) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        print("errors:", errors)
    """)
    assert "errors: []" in out


def test_dynamic_override_discovery(tmp_path):
    """A new override module is blended at runtime — no regeneration needed."""
    import pathlib

    import b1sl.b1sl.models._overrides as ov

    override_file = pathlib.Path(ov.__path__[0]) / "_tmp_test_override.py"
    override_file.write_text(textwrap.dedent("""
        from .._generated.entities.finance import Currency as _Currency

        class Currency(_Currency):
            @property
            def marker(self) -> str:
                return "dynamic"
    """))
    try:
        out = run_py("""
            from b1sl.b1sl import entities as en
            print("marker:", en.Currency(code="USD").marker)
        """)
    finally:
        override_file.unlink()
    assert "marker: dynamic" in out


def test_non_subclass_shadow_warns_and_is_ignored(tmp_path):
    import pathlib

    import b1sl.b1sl.models._overrides as ov

    override_file = pathlib.Path(ov.__path__[0]) / "_tmp_test_bad_override.py"
    override_file.write_text("class Currency:\n    pass\n")
    try:
        out = run_py("""
            import logging

            records = []

            class Capture(logging.Handler):
                def emit(self, record):
                    records.append(record.getMessage())

            logging.getLogger("b1sl").addHandler(Capture())

            from b1sl.b1sl import entities as en
            currency = en.Currency(code="USD")
            print("still generated model:", currency.code)
            print("warned:", any("does not subclass it" in m for m in records))
        """)
    finally:
        override_file.unlink()
    assert "still generated model: USD" in out
    assert "warned: True" in out


def test_preload_builds_everything():
    out = run_py("""
        from b1sl.b1sl import entities as en
        from b1sl.b1sl.models._generated import entities as gen

        en.preload()
        # master_namespace() is the override-aware mapping; _ALL_MODELS keeps
        # the generated base classes, which stay unbuilt when overridden.
        incomplete = [
            m.__name__
            for m in gen.master_namespace().values()
            if not m.__pydantic_complete__
        ]
        print("incomplete:", incomplete)
    """)
    assert "incomplete: []" in out
