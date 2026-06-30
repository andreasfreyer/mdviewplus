"""Zentrales Logging — ab Tag 1, damit Fehler im Feld nachvollziehbar sind."""

from __future__ import annotations

import logging
import os


def setup_logging(verbose: bool = False) -> logging.Logger:
    """Initialisiert das Root-Logging. DEBUG via --verbose oder MDVIEWPLUS_DEBUG=1."""
    level = logging.DEBUG if (verbose or os.environ.get("MDVIEWPLUS_DEBUG")) else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    return logging.getLogger("mdviewplus")
