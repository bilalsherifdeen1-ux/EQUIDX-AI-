"""Structured JSON logging configuration (structlog), shipped to stdout for
collection by the ELK/OpenSearch pipeline (see infrastructure/logging)."""
import logging
import sys

import structlog


def configure_logging(log_level: str = "info") -> None:
    logging.basicConfig(
        format="%(message)s", stream=sys.stdout, level=log_level.upper()
    )
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.getLevelName(log_level.upper())
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str):
    return structlog.get_logger(name)
