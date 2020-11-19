import sys
import subprocess
import webbrowser

# pylint: disable=import-error
from ankisync2.dir import AnkiPath


if __name__ == "__main__":
    anki_path = AnkiPath()
    anki_path.show()
