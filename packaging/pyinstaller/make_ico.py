"""Erzeugt packaging/mdviewplus.ico aus dem PNG — fuer das Windows-.exe-Icon.

Wird nur im Windows-CI-Job gebraucht (PyInstaller --icon will .ico). Auf Linux
nutzt das AppImage direkt die PNG.
"""

from pathlib import Path

from PIL import Image

root = Path(__file__).resolve().parents[2]
png = root / "src" / "mdviewplus" / "mdviewplus.png"
ico = root / "packaging" / "mdviewplus.ico"

img = Image.open(png).convert("RGBA")
img.save(ico, sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
print("geschrieben:", ico)
