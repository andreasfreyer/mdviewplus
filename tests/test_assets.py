"""Tests fuer die Aufloesung der gebuendelten Assets."""

from mdviewplus.assets import VENDOR_FILES, vendor_dir


def test_vendor_files_present_and_nonempty():
    path = vendor_dir()
    for name in VENDOR_FILES:
        f = path / name
        assert f.is_file(), f"{name} fehlt"
        assert f.stat().st_size > 0, f"{name} ist leer"


def test_vendor_contains_expected_globals():
    path = vendor_dir()
    mdit = (path / "markdown-it.min.js").read_text(encoding="utf-8", errors="ignore")
    assert "markdownit" in mdit
    mermaid = (path / "mermaid.min.js").read_text(encoding="utf-8", errors="ignore")
    assert "mermaid" in mermaid
