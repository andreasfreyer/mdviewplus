#!/usr/bin/env bash
#
# Baut ein schlankes natives .deb. Kein Bundling von Qt — das Paket setzt auf die
# Qt-Pakete der Distribution auf (python3-pyqt6 + qtwebengine), enthaelt also nur
# unseren Python-Code + die vendored JS-Libs (~3 MB). Beste Einbettung auf
# Debian/Ubuntu/Kubuntu: App-Menue-Eintrag, Icon, MIME-Verknuepfung; apt verwaltet
# die Qt-Abhaengigkeiten und Updates mit.
#
# Aufruf:  bash packaging/deb/build-deb.sh
# Ergebnis: mdviewplus_<version>_all.deb im Projektwurzel-Verzeichnis.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VERSION="$(grep -oP '__version__\s*=\s*"\K[^"]+' "${ROOT}/src/mdviewplus/__init__.py")"
ARCH=all
PKG="mdviewplus_${VERSION}_${ARCH}"
BUILD="${ROOT}/dist/deb/${PKG}"

[ -n "${VERSION}" ] || { echo "FEHLER: Version nicht aus __init__.py lesbar."; exit 1; }

rm -rf "${BUILD}"

# --- Python-Paket nach dist-packages (auf sys.path jedes Debian-python3) -----
SITE="${BUILD}/usr/lib/python3/dist-packages/mdviewplus"
mkdir -p "${SITE}/vendor"
cp "${ROOT}"/src/mdviewplus/*.py            "${SITE}/"
cp "${ROOT}/src/mdviewplus/mdviewplus.png"  "${SITE}/"
cp "${ROOT}"/src/mdviewplus/vendor/*.js     "${SITE}/vendor/"

# --- Launcher auf PATH ------------------------------------------------------
mkdir -p "${BUILD}/usr/bin"
cat > "${BUILD}/usr/bin/mdviewplus" <<'EOF'
#!/bin/sh
exec python3 -m mdviewplus "$@"
EOF
chmod 755 "${BUILD}/usr/bin/mdviewplus"

# --- Desktop-Integration: Menue-Eintrag, Icon ------------------------------
install -Dm644 "${ROOT}/packaging/mdviewplus.desktop" \
  "${BUILD}/usr/share/applications/mdviewplus.desktop"
install -Dm644 "${ROOT}/src/mdviewplus/mdviewplus.png" \
  "${BUILD}/usr/share/icons/hicolor/256x256/apps/mdviewplus.png"

# --- Metadaten (control) ----------------------------------------------------
mkdir -p "${BUILD}/DEBIAN"
INSTALLED_KB="$(du -ks "${BUILD}/usr" | cut -f1)"
cat > "${BUILD}/DEBIAN/control" <<EOF
Package: mdviewplus
Version: ${VERSION}
Architecture: ${ARCH}
Maintainer: Andreas Freyer <freyer@online.de>
Installed-Size: ${INSTALLED_KB}
Depends: python3 (>= 3.10), python3-pyqt6, python3-pyqt6.qtwebengine
Section: utils
Priority: optional
Homepage: https://github.com/andreasfreyer/mdviewplus
Description: Nativer Qt6-Markdown-Viewer mit Mermaid und Live-Reload
 mdviewplus rendert Markdown-Dateien mit eingebetteten Mermaid-Diagrammen
 inline und an der richtigen Stelle, mit Live-Reload und vollstaendig offline
 (markdown-it + mermaid sind im Paket gebuendelt). Reiner Viewer; die Datei
 des Nutzers wird nie editiert.
EOF

# --- Maintainer-Skripte: Caches aktualisieren, Bytecode kompilieren ---------
cat > "${BUILD}/DEBIAN/postinst" <<'EOF'
#!/bin/sh
set -e
if command -v py3compile >/dev/null 2>&1; then
  py3compile -p mdviewplus || true
fi
if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database -q /usr/share/applications || true
fi
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
  gtk-update-icon-cache -q -f /usr/share/icons/hicolor || true
fi
EOF
chmod 755 "${BUILD}/DEBIAN/postinst"

cat > "${BUILD}/DEBIAN/prerm" <<'EOF'
#!/bin/sh
set -e
if command -v py3clean >/dev/null 2>&1; then
  py3clean -p mdviewplus || true
fi
EOF
chmod 755 "${BUILD}/DEBIAN/prerm"

# --- Packen -----------------------------------------------------------------
OUT="${ROOT}/${PKG}.deb"
dpkg-deb --build --root-owner-group "${BUILD}" "${OUT}"
echo "deb gebaut: ${OUT}"
