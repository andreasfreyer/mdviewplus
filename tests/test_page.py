"""Tests fuer den Qt-freien Page-Renderer."""

from mdviewplus.page import build_page_html


def test_loads_vendored_scripts():
    html = build_page_html(dark=False)
    assert '<script src="markdown-it.min.js"></script>' in html
    assert '<script src="mermaid.min.js"></script>' in html


def test_theme_switch():
    assert 'theme: "default"' in build_page_html(dark=False)
    assert 'theme: "dark"' in build_page_html(dark=True)


def test_mermaid_fence_handling_present():
    html = build_page_html(dark=False)
    assert 'class="mermaid"' in html
    assert 'lang === "mermaid"' in html


def test_exposes_render_function():
    assert "window.renderMarkdown" in build_page_html(dark=False)


def test_mermaid_starts_off():
    # startOnLoad muss false sein — gerendert wird erst, wenn der Viewer Text liefert.
    assert "startOnLoad: false" in build_page_html(dark=False)
