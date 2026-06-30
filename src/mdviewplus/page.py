"""Baut die statische HTML-Seite, die das Rendering im QWebEngineView macht.

Reine Funktion, Qt-frei -> unit-testbar. Die Seite lädt die gebündelten Libs
(relativ zur baseUrl = vendor/) und stellt window.renderMarkdown(text) bereit,
das der Viewer bei jedem (Neu-)Laden der Datei aufruft.
"""

from __future__ import annotations


def build_page_html(dark: bool) -> str:
    """Erzeugt die Viewer-Seite. `dark` schaltet Theme (CSS + Mermaid) um."""
    theme = "dark" if dark else "default"
    bg = "#1e1e1e" if dark else "#ffffff"
    fg = "#e0e0e0" if dark else "#1a1a1a"
    code_bg = "#2a2a2a" if dark else "#f4f4f4"
    border = "#444" if dark else "#dddddd"

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script src="markdown-it.min.js"></script>
<script src="mermaid.min.js"></script>
<style>
  body {{
    background: {bg}; color: {fg};
    font-family: system-ui, "Noto Sans", sans-serif;
    line-height: 1.6; max-width: 860px;
    margin: 0 auto; padding: 2.5rem 2rem 6rem;
  }}
  h1, h2, h3, h4 {{ line-height: 1.25; margin-top: 1.8em; }}
  h1 {{ border-bottom: 2px solid {border}; padding-bottom: .3em; }}
  h2 {{ border-bottom: 1px solid {border}; padding-bottom: .2em; }}
  a {{ color: #3a86ff; }}
  code {{ background: {code_bg}; padding: .15em .4em; border-radius: 4px;
          font-family: "JetBrains Mono", "Fira Code", monospace; font-size: .9em; }}
  pre {{ background: {code_bg}; border-radius: 8px; }}
  pre code {{ display: block; padding: 1em; overflow-x: auto; background: none; }}
  blockquote {{ border-left: 4px solid {border}; margin: 1em 0; padding: .2em 1em; opacity: .85; }}
  table {{ border-collapse: collapse; }}
  th, td {{ border: 1px solid {border}; padding: .4em .8em; }}
  hr {{ border: none; border-top: 1px solid {border}; margin: 2em 0; }}
  img {{ max-width: 100%; }}
  .mermaid {{ background: transparent; text-align: center; margin: 1.5em 0; }}
  .mdv-error {{ color: #c0392b; font-family: monospace; white-space: pre-wrap;
               border: 1px solid #c0392b; border-radius: 6px; padding: .6em 1em; }}
</style>
</head>
<body>
<div id="content"></div>
<script>
  const md = window.markdownit({{ html: true, linkify: true, typographer: true }});

  function esc(s) {{
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }}

  // Fenced-Code-Renderer: ```mermaid -> <pre class="mermaid">, sonst normaler Code-Block.
  md.renderer.rules.fence = (tokens, idx) => {{
    const t = tokens[idx];
    const lang = (t.info || "").trim().split(/\\s+/)[0];
    if (lang === "mermaid") {{
      // nur & und < maskieren; textContent dekodiert sie fuer Mermaid wieder korrekt.
      const code = t.content.replace(/&/g, "&amp;").replace(/</g, "&lt;");
      return '<pre class="mermaid">' + code + "</pre>";
    }}
    const cls = lang ? ' class="language-' + lang + '"' : "";
    return "<pre><code" + cls + ">" + esc(t.content) + "</code></pre>";
  }};

  mermaid.initialize({{ startOnLoad: false, theme: "{theme}", securityLevel: "loose" }});

  // Wird vom Viewer bei jedem (Neu-)Laden aufgerufen. Scrollposition bleibt erhalten.
  window.renderMarkdown = function (text) {{
    const y = window.scrollY;
    try {{
      document.getElementById("content").innerHTML = md.render(text);
    }} catch (e) {{
      document.getElementById("content").innerHTML =
        '<div class="mdv-error">Markdown-Fehler: ' + esc(String(e)) + "</div>";
      return;
    }}
    mermaid.run({{ querySelector: ".mermaid" }})
      .then(() => window.scrollTo(0, y))
      .catch((e) => {{ console.error(e); window.scrollTo(0, y); }});
  }};
</script>
</body>
</html>"""
