"""
b1sl.b1sl.environment — Runtime environment type definition.

Provides a strongly-typed ``B1Env`` enum that centralises the concept of
"which deployment stage is this process running in?" instead of scattering
raw ``os.getenv("B1SL_ENV")`` calls across the SDK.

Usage::

    from b1sl.b1sl import B1Env

    config = B1Config.from_env()        # reads B1SL_ENV automatically
    assert config.environment == B1Env.PROD
"""

from enum import Enum


class B1Env(str, Enum):
    """
    Deployment-stage identifier for a B1SL process.

    Because ``B1Env`` inherits from ``str``, instances compare equal to their
    string counterparts::

        B1Env.PROD == "prod"   # True — safe to use in logging, serialisation, etc.

    Attributes:
        DEV:  Local development.  Human-readable log output, relaxed SSL defaults.
        TEST: Automated test runs. Identical to DEV but signals test isolation.
        PROD: Production workload. Structured JSON logging enabled automatically.
    """

    DEV = "dev"
    TEST = "test"
    PROD = "prod"
