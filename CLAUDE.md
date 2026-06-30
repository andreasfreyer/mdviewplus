# CLAUDE.md — mdviewplus

Projektkontext für künftige CW/CC-Sessions. Bewusst **schlank** gehalten (KISS);
dies ist ein kleines Tool, kein Bellrinx-Workstream.

## Was es ist

Nativer Qt6-Markdown-Viewer mit Mermaid, Live-Reload, offline. Reiner Viewer —
editiert nie die Datei des Nutzers.

## Architektur (alle Module klein, eine Verantwortung)

| Datei | Verantwortung |
|-------|---------------|
| `cli.py` | argparse, Logging-Init, App-Start. Qt erst hier importiert (`--version`/`--help` ohne Display). |
| `assets.py` | Auflösung der **gebündelten** vendor/-Libs. Kein Download. |
| `page.py` | **Qt-freie** reine Funktion `build_page_html(dark)` → HTML/JS. Unit-getestet. |
| `viewer.py` | `QWebEngineView` + `QFileSystemWatcher` (Live-Reload, entprellt). |
| `log.py` | Logging ab Tag 1. |
| `vendor/` | markdown-it.min.js (14.1.0) + mermaid.min.js (11.4.1), MIT. |

## Render-Fluss

1. `viewer` lädt einmalig `build_page_html()` mit `baseUrl = vendor/` (lädt die Libs lokal).
2. Bei jedem (Neu-)Laden der Datei ruft `viewer.push()` → `renderMarkdown(text)` in der Seite.
3. markdown-it rendert MD → HTML; ```mermaid-Blöcke werden zu `<pre class="mermaid">`;
   danach `mermaid.run()`. Scrollposition bleibt erhalten.

## Bewusste Entscheidungen

- **Vendoring statt CDN/Download**: Offline ab Installation, deterministisch.
  Update = neue Datei in `vendor/` legen, Version in README/CLAUDE anpassen.
- **`securityLevel: "loose"`** in mermaid.initialize: erlaubt volle Mermaid-Features.
  Vertretbar, da der Nutzer eigene, vertrauenswürdige Dateien öffnet. Bei Bedarf für
  fremde Dateien auf `"strict"` umstellen.
- **Reiner Viewer**, kein Editor: vermeidet das MarkText-Problem (Reformatieren der Quelle).
  Editiert wird im gewohnten Editor (z. B. Kate), mdviewplus zeigt nur an.

## Tests

`pytest` — Unit-Tests auf `page.py` (Qt-frei) und `assets.py`. Die Qt-GUI wird
nicht headless getestet (bewusst; kein Mehrwert für ein Tool dieser Größe).
Vor Push: Tests grün, manuelle Sichtprüfung mit `examples/mermaid-render-test.md`.

## Git-Workflow

Direkt auf `main`, mehrere logische Commits, keine PRs (1 Mensch + AI). Wrap-up
mit `git show --stat`.

## Mögliche Erweiterungen (nicht jetzt — KISS)

TOC-Sidebar, Druck/PDF-Export, Theme aus Datei, SHA256-Pinning der vendor-Libs.
Jede Erweiterung muss ihren Daseinsgrund beweisen, bevor sie reinkommt.
