"""Das Qt-Fenster: QWebEngineView + Live-Reload via QFileSystemWatcher."""

from __future__ import annotations

import json
import logging
from importlib import resources
from pathlib import Path

from PyQt6.QtCore import QUrl, QFileSystemWatcher, QTimer
from PyQt6.QtGui import QIcon, QPalette
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings

from .page import build_page_html

log = logging.getLogger("mdviewplus.viewer")


class Viewer(QMainWindow):
    """Zeigt eine Markdown-Datei gerendert an und lädt bei Änderung neu."""

    def __init__(self, path: Path, dark: bool, vendor: Path):
        super().__init__()
        self.path = path
        self.setWindowTitle(f"{path.name} — mdviewplus")
        self.setWindowIcon(_app_icon())
        self.resize(960, 1000)

        self.view = QWebEngineView()
        self.setCentralWidget(self.view)

        settings = self.view.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, False)

        self._ready = False
        self.view.loadFinished.connect(self._on_loaded)

        # baseUrl = vendor/ -> <script src="mermaid.min.js"> findet die gebündelten Libs.
        base = QUrl.fromLocalFile(str(vendor) + "/")
        self.view.setHtml(build_page_html(dark), base)

        # Live-Reload mit Entprellung (Editoren feuern oft mehrere Events pro Speichern).
        self.watcher = QFileSystemWatcher([str(path)])
        self.watcher.fileChanged.connect(self._on_file_changed)
        self._debounce = QTimer(self)
        self._debounce.setSingleShot(True)
        self._debounce.setInterval(120)
        self._debounce.timeout.connect(self.push)

    def _on_loaded(self, ok: bool) -> None:
        self._ready = bool(ok)
        if ok:
            self.push()
        else:
            log.error("Seite konnte nicht geladen werden")

    def _on_file_changed(self, _path: str) -> None:
        # Atomare Speichervorgänge ersetzen die Datei -> Pfad ggf. neu beobachten.
        if str(self.path) not in self.watcher.files():
            self.watcher.addPath(str(self.path))
        self._debounce.start()

    def push(self) -> None:
        """Liest die Datei und schickt ihren Inhalt an die Render-Funktion der Seite."""
        if not self._ready:
            return
        try:
            text = self.path.read_text(encoding="utf-8", errors="replace")
        except FileNotFoundError:
            log.warning("Datei nicht gefunden (vorübergehend?): %s", self.path)
            return
        log.debug("rendere %d Zeichen", len(text))
        self.view.page().runJavaScript(f"renderMarkdown({json.dumps(text)})")


def _app_icon() -> QIcon:
    """Lädt das gebündelte Fenstericon aus dem Paket (leer, falls es fehlt)."""
    try:
        path = resources.files("mdviewplus") / "mdviewplus.png"
        return QIcon(str(path))
    except (FileNotFoundError, ModuleNotFoundError):
        return QIcon()


def is_dark(app: QApplication) -> bool:
    """Erkennt anhand der Qt-Palette, ob ein dunkles Theme aktiv ist."""
    return app.palette().color(QPalette.ColorRole.Window).lightness() < 128
