import logging


def get_test_logger(name="test_logger", level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        # Create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(level)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Add formatter to ch
        ch.setFormatter(formatter)

        # Add ch to logger
        logger.addHandler(ch)

    return logger
