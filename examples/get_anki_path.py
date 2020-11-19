import sys
import subprocess
import webbrowser

from ankisync2.dir import AnkiPath  # pylint: disable=import-error


if __name__ == "__main__":
    anki_path = AnkiPath()
    anki_path.show()
