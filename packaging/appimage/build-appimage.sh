#!/usr/bin/env bash
#
# Wrappt die PyInstaller-onedir-Ausgabe (dist/mdviewplus/) in ein AppImage.
# PyInstaller hat das schwere Qt/WebEngine-Bundling schon erledigt — hier wird
# das Ergebnis nur noch in eine AppDir-Struktur gelegt und mit appimagetool
# zu einer portablen Datei gepackt.
#
# Aufruf:  bash packaging/appimage/build-appimage.sh [ausgabename.AppImage]
# Voraussetzung: PyInstaller lief bereits -> dist/mdviewplus/ existiert.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DIST="${ROOT}/dist/mdviewplus"
APPDIR="${ROOT}/AppDir"
OUT="${1:-mdviewplus-x86_64.AppImage}"

[ -d "${DIST}" ] || { echo "FEHLER: ${DIST} fehlt — erst PyInstaller laufen lassen."; exit 1; }

# --- AppDir aufbauen --------------------------------------------------------
rm -rf "${APPDIR}"
mkdir -p "${APPDIR}/usr/bin"
cp -a "${DIST}/." "${APPDIR}/usr/bin/"

# Icon + Desktop ins AppDir-Root (appimagetool erwartet beides dort)
cp "${ROOT}/src/mdviewplus/mdviewplus.png" "${APPDIR}/mdviewplus.png"
cp "${ROOT}/packaging/mdviewplus.desktop"  "${APPDIR}/mdviewplus.desktop"
install -Dm644 "${ROOT}/src/mdviewplus/mdviewplus.png" \
  "${APPDIR}/usr/share/icons/hicolor/256x256/apps/mdviewplus.png"

# AppRun: startet die PyInstaller-Binary, leitet Argumente (die .md-Datei) durch.
cat > "${APPDIR}/AppRun" <<'EOF'
#!/bin/bash
HERE="$(dirname "$(readlink -f "${0}")")"
# Die Chromium-Sandbox von QtWebEngine braucht einen setuid-Helfer, den ein
# portables AppImage nicht bereitstellen kann -> deaktivieren. Vertretbar, da
# der Nutzer eigene, vertrauenswuerdige Dateien oeffnet.
export QTWEBENGINE_DISABLE_SANDBOX=1
exec "${HERE}/usr/bin/mdviewplus" "$@"
EOF
chmod +x "${APPDIR}/AppRun"

# --- appimagetool holen & packen -------------------------------------------
TOOL="${ROOT}/appimagetool.AppImage"
if [ ! -f "${TOOL}" ]; then
  curl -fsSL -o "${TOOL}" \
    "https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage"
  chmod +x "${TOOL}"
fi

# GitHub-Runner haben kein FUSE -> AppImages selbst entpacken statt mounten.
export APPIMAGE_EXTRACT_AND_RUN=1
ARCH=x86_64 "${TOOL}" "${APPDIR}" "${OUT}"
echo "AppImage gebaut: ${OUT}"
