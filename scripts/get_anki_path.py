import os
import sys
import subprocess
import webbrowser

from appdirs import AppDirs


def get_anki_path(user: str) -> str:
    """
    Most reliable way is to go to
    Tools >> Add-ons >> View Files
    """

    if os.name == "posix":
        "Linux or macOS"

        a = AppDirs("Anki2")
        return os.path.join(a.user_data_dir, user)
    else:
        "Windows"

        raise NotImplementedError()


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
