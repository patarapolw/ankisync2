import sys
import subprocess
import webbrowser

# pylint: disable=import-error
from ankisync2.dir import get_anki_path


if __name__ == "__main__":
    anki_path = get_anki_path("User 1")

    try:
        subprocess.call(
            [
                {"darwin": "open", "linux": "xdg-open", "win32": "explorer"}[
                    sys.platform
                ],
                anki_path,
            ]
        )
    except KeyError:
        webbrowser.open(f"file://${anki_path}")
