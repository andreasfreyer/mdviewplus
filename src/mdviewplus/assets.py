"""Auflösung der gebündelten JS-Assets (markdown-it + mermaid).

Bewusste Design-Entscheidung: Die Libraries werden ins Paket *vendored*, nicht
zur Laufzeit geladen. Damit läuft mdviewplus ab Installation vollständig offline
und deterministisch — kein CDN, kein "erster Start braucht Netz".
"""

from __future__ import annotations

import logging
from importlib import resources
from pathlib import Path

log = logging.getLogger("mdviewplus.assets")

# Skript-Dateinamen, die die HTML-Seite per <script src="..."> erwartet.
VENDOR_FILES = ("markdown-it.min.js", "mermaid.min.js")


def vendor_dir() -> Path:
    """Liefert den Pfad zum gebündelten vendor/-Ordner.

    Raises:
        FileNotFoundError: wenn ein erwartetes Asset fehlt (kaputte Installation).
    """
    base = resources.files("mdviewplus") / "vendor"
    path = Path(str(base))
    missing = [name for name in VENDOR_FILES if not (path / name).is_file()]
    if missing:
        raise FileNotFoundError(
            f"Gebündelte Assets fehlen in {path}: {', '.join(missing)}. "
            "Paket neu installieren oder vendor/-Dateien wiederherstellen."
        )
    log.debug("vendor dir: %s", path)
    return path
