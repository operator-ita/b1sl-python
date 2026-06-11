"""Sync/async surface parity (CLAUDE.md contract).

Every sync class has an async counterpart and "both surfaces must support the
same parameters and methods". These tests turn that contract into an
executable check: any drift (a method added on one side only, or a parameter
renamed/added asymmetrically) fails here instead of slipping into a release.
"""
from __future__ import annotations

import inspect

import pytest

from b1sl.b1sl.async_client import AsyncB1Client
from b1sl.b1sl.async_rest_adapter import AsyncRestAdapter
from b1sl.b1sl.client import B1Client
from b1sl.b1sl.resources.async_base import AsyncGenericResource
from b1sl.b1sl.resources.base import GenericResource
from b1sl.b1sl.resources.odata import AsyncQueryBuilder, QueryBuilder
from b1sl.b1sl.rest_adapter import RestAdapter

# Name translations between the two surfaces (sync name → async name).
NAME_MAP = {"close": "aclose"}

# Members that legitimately exist on only one side.
SYNC_ONLY: dict[type, set[str]] = {
    RestAdapter: {
        "handle_token",  # decorator infrastructure; async uses _request()
        "session",       # raw httpx.Client attribute
    },
}
ASYNC_ONLY: dict[type, set[str]] = {
    AsyncRestAdapter: {
        "connect",         # async client pool must be created in a running loop
        "ensure_session",  # async login coordination (sync uses the decorator)
    },
}

# Parameters that legitimately differ for a given (class, method).
PARAM_EXCEPTIONS: dict[tuple[str, str], set[str]] = {}


def public_members(cls: type) -> set[str]:
    return {
        name
        for name, member in inspect.getmembers(cls)
        if not name.startswith("_") and (callable(member) or isinstance(member, property))
    }


def normalized(names: set[str]) -> set[str]:
    return {NAME_MAP.get(n, n) for n in names}


PAIRS = [
    (B1Client, AsyncB1Client),
    (GenericResource, AsyncGenericResource),
    (QueryBuilder, AsyncQueryBuilder),
    (RestAdapter, AsyncRestAdapter),
]


@pytest.mark.parametrize("sync_cls,async_cls", PAIRS, ids=lambda c: c.__name__)
def test_public_member_sets_match(sync_cls, async_cls):
    sync_members = public_members(sync_cls) - SYNC_ONLY.get(sync_cls, set())
    async_members = public_members(async_cls) - ASYNC_ONLY.get(async_cls, set())

    missing_in_async = normalized(sync_members) - async_members
    missing_in_sync = async_members - normalized(sync_members)

    assert not missing_in_async, (
        f"{async_cls.__name__} lacks members present on {sync_cls.__name__}: "
        f"{sorted(missing_in_async)}"
    )
    assert not missing_in_sync, (
        f"{sync_cls.__name__} lacks members present on {async_cls.__name__}: "
        f"{sorted(missing_in_sync)}"
    )


@pytest.mark.parametrize("sync_cls,async_cls", PAIRS, ids=lambda c: c.__name__)
def test_shared_method_signatures_match(sync_cls, async_cls):
    """Shared public methods must accept the same parameter names, in order."""
    sync_members = public_members(sync_cls) - SYNC_ONLY.get(sync_cls, set())

    drift: list[str] = []
    for name in sorted(sync_members):
        async_name = NAME_MAP.get(name, name)
        sync_attr = inspect.getattr_static(sync_cls, name)
        async_attr = inspect.getattr_static(async_cls, async_name, None)
        if async_attr is None:
            continue  # covered by the member-set test
        if isinstance(sync_attr, property) or isinstance(async_attr, property):
            continue  # properties take no parameters

        try:
            sync_params = list(inspect.signature(getattr(sync_cls, name)).parameters)
            async_params = list(
                inspect.signature(getattr(async_cls, async_name)).parameters
            )
        except (TypeError, ValueError):
            continue

        allowed = PARAM_EXCEPTIONS.get((sync_cls.__name__, name), set())
        s = [p for p in sync_params if p not in allowed]
        a = [p for p in async_params if p not in allowed]
        if s != a:
            drift.append(f"{name}: sync{s} != async{a}")

    assert not drift, (
        f"Signature drift between {sync_cls.__name__} and {async_cls.__name__}:\n"
        + "\n".join(drift)
    )
