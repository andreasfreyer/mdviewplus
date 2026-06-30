"""Kommandozeilen-Einstieg: mdviewplus <datei.md>."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .assets import vendor_dir
from .log import setup_logging


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="mdviewplus",
        description="Nativer Qt6-Markdown-Viewer mit Mermaid und Live-Reload.",
    )
    parser.add_argument("file", help="Pfad zur .md-Datei")
    parser.add_argument("--version", action="version", version=f"mdviewplus {__version__}")
    parser.add_argument("-v", "--verbose", action="store_true", help="Debug-Logging")
    theme = parser.add_mutually_exclusive_group()
    theme.add_argument("--dark", action="store_true", help="Dark-Theme erzwingen")
    theme.add_argument("--light", action="store_true", help="Light-Theme erzwingen")
    args = parser.parse_args()

    log = setup_logging(args.verbose)

    path = Path(args.file).expanduser().resolve()
    if not path.is_file():
        sys.exit(f"mdviewplus: Datei nicht gefunden: {path}")

    try:
        vendor = vendor_dir()
    except FileNotFoundError as exc:
        sys.exit(f"mdviewplus: {exc}")

    # Qt erst hier importieren, damit --version/--help ohne Display funktionieren.
    from PyQt6.QtWidgets import QApplication
    from .viewer import Viewer, is_dark

    app = QApplication(sys.argv)
    dark = True if args.dark else False if args.light else is_dark(app)
    log.debug("theme=%s", "dark" if dark else "light")

    win = Viewer(path, dark, vendor)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
