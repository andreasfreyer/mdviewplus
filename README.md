# mdviewplus

Ein **nativer Qt6-Markdown-Viewer** für Linux mit korrekter **Mermaid-Darstellung**,
**Live-Reload** und **vollständigem Offline-Betrieb**.

Entstanden aus einem konkreten Ärgernis: Kein verbreitetes Tool rendert eine
Markdown-Datei mit eingebetteten Mermaid-Diagrammen zuverlässig **an der richtigen
Stelle** — die einen reformatieren die Datei (MarkText), andere crashen (Obsidian),
native Qt-Tools können Mermaid prinzipbedingt nicht (ghostwriter, Okular), und junge
Eigenrenderer schieben Diagramme an den Seitenanfang (Ferrite).

## Warum eine Web-Engine?

Mermaid ist eine JavaScript-Library. Jedes Tool, das Mermaid **grafisch** rendert,
braucht eine Web-Engine. mdviewplus nutzt deshalb `QWebEngineView` — aber als
schlankes, eigenes Qt-Fenster, nicht als Browser-Tab und nicht als 300-MB-Electron.
Das Rendering selbst macht **markdown-it + mermaid**, beide ins Paket gebündelt.

## Features

- Korrekte **Inline-Darstellung** von Mermaid-Diagrammen (an Ort und Stelle, in Reihenfolge)
- **Offline ab Installation** — keine CDN, kein Laufzeit-Download (Libs sind vendored)
- **Live-Reload**: Datei in deinem Editor speichern → Fenster aktualisiert sich
- **Reiner Viewer**: editiert/reformatiert deine Datei nie
- Auto Dark/Light nach Qt-Palette (`--dark` / `--light` erzwingbar)

## Installation (Kubuntu/Debian)

```bash
# Qt-Abhängigkeiten nativ (empfohlen auf KDE):
sudo apt install python3-pyqt6 python3-pyqt6.qtwebengine

# Paket installieren:
pip install --user .
# oder isoliert:
pipx install .
```

## Nutzung

```bash
mdviewplus examples/mermaid-render-test.md
mdviewplus --dark pfad/zu/datei.md
```

## Als Standard-Viewer für .md registrieren

```bash
cp packaging/mdviewplus.desktop ~/.local/share/applications/
update-desktop-database ~/.local/share/applications 2>/dev/null
xdg-mime default mdviewplus.desktop text/markdown text/x-markdown
```

## Entwicklung

```bash
pip install --user -e ".[dev]"
pytest
```

Architektur und Konventionen: siehe [CLAUDE.md](CLAUDE.md).

## Lizenz

MIT — siehe [LICENSE](LICENSE). Bündelt markdown-it und mermaid (beide MIT).
