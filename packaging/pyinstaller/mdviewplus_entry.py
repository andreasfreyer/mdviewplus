"""PyInstaller-Einstiegspunkt.

PyInstaller braucht ein Skript als Startpunkt; `python -m mdviewplus` geht nicht
direkt. Dieses Skript ruft einfach die normale CLI-main() auf — die gesamte Logik
bleibt im Paket. Die gebündelten Assets (vendor/*.js, mdviewplus.png) werden im
Build per `--collect-data mdviewplus` mit eingepackt.
"""

from mdviewplus.cli import main

if __name__ == "__main__":
    main()
