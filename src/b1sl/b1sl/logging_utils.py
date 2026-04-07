import json
import logging
import os
from datetime import datetime, timezone

from b1sl.b1sl.environment import B1Env


class B1JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for SAP B1 SDK logs.

    AI Role: Highly recommended for automated log parsing (ELK, Datadog).
    It structure key metadata into top-level JSON fields for efficient filtering.

    The fields included are:
        - timestamp (ISO 8601 with Z)
        - level (LogLevel)
        - logger (Logger name)
        - message (Log text)
        - req_id (Tracing ID)
        - user (SAP B1 User)
        - db (Company Database)
        - session_id (SAP Session)
        - http_method
        - endpoint
        - status_code
        - sap_error
    """

    def format(self, record):
        """
        Formats a LogRecord into a JSON string.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: JSON string containing standard and extra fields.
        """
        log_record = {
            "timestamp": datetime.now(timezone.utc).replace(tzinfo=None).isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Extract structured fields from 'extra' if provided
        for field in [
            "req_id",
            "user",
            "db",
            "session_id",
            "sap_error",
            "http_method",
            "endpoint",
            "status_code",
        ]:
            if hasattr(record, field):
                log_record[field] = getattr(record, field)

        # Include exception info if present
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record)


def setup_logging(
    level: int = logging.INFO,
    *,
    env: B1Env | None = None,
) -> logging.Logger:
    """
    Initialise the SAP B1 SDK logger with environment-aware formatting.

    ⚠️ WARNING: FOR STANDALONE SCRIPTS ONLY ⚠️
    This function configures handlers and formatters on the root "b1sl" logger.
    If you are using this SDK inside a framework (FastAPI, Django, etc.) that
    manages its own logging, DO NOT call this function. It will conflict with
    your host application's handlers. The SDK adheres to standard Python library
    logging and will naturally propagate to your app's root logger.

    Log format by environment:
        - ``B1Env.PROD``: Structured JSON via :class:`B1JSONFormatter`.
        - ``B1Env.DEV`` / ``B1Env.TEST``: Human-readable text.

    Args:
        level (int, optional): Logging verbosity. Defaults to INFO.
        env (B1Env, optional): Explicit environment override. When omitted,
            reads ``B1SL_ENV`` (default: ``dev``).

    Returns:
        logging.Logger: The configured ``b1sl`` root logger.

    Example::

        env = B1Environment.load()
        setup_logging(env=env.config.environment)
    """
    resolved_env = env or B1Env(os.getenv("B1SL_ENV", "dev").lower())

    logger = logging.getLogger("b1sl")
    logger.setLevel(level)

    if logger.hasHandlers():
        logger.handlers.clear()

    handler = logging.StreamHandler()

    if resolved_env == B1Env.PROD:
        handler.setFormatter(B1JSONFormatter())
    else:
        # DEV / TEST: readable and concise
        formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
        handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
