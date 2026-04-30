"""Utils para logging."""

import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"


def configure_logging(level=logging.INFO):
    """Configura o logging com um formato consistente."""

    logging.basicConfig(level=level, format=LOG_FORMAT)
