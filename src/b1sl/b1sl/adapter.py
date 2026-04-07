from __future__ import annotations

import logging

from b1sl.b1sl.config import B1Config
from b1sl.b1sl.rest_adapter import RestAdapter

# ── Legacy Django-only shared adapter ──────────────────────────────────────
# Prefer B1Client (via web/services/b1sl.py) for all new code.
# This module exists only for the legacy *_endpoint.py classes that have not
# yet been migrated to constructor-injected RestAdapter.
#
# NOTE: RestAdapter is no longer a Singleton. This module-level global IS the
# single shared instance for legacy endpoints. Do not instantiate RestAdapter
# directly in endpoint classes.

_logger = logging.getLogger(__name__)
_rest_adapter: RestAdapter | None = None


def get_rest_adapter() -> RestAdapter:
    """Return (or lazily create) the shared Django adapter instance."""
    global _rest_adapter
    if _rest_adapter is None:
        _rest_adapter = RestAdapter.from_config(B1Config.from_django_settings())
    return _rest_adapter


# Eager init — fails silently if Django settings are not ready yet.
# Legacy endpoints that import `rest_adapter` directly will get None until
# settings are fully loaded; get_rest_adapter() will correct this on first call.
try:
    rest_adapter = get_rest_adapter()
except Exception as _e:
    _logger.warning(
        "b1sl.b1sl.adapter: could not eagerly initialise rest_adapter "
        f"({_e!r}). Legacy endpoints will fail until Django settings are ready. "
        "Call get_rest_adapter() explicitly after settings are loaded."
    )
    rest_adapter = None
