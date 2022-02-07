import os
import sys
from pathlib import Path
import subprocess


class AnkiPath:
    """Get User's Anki path

    Most reliable way is to go to
    `Tools >> Add-ons >> View Files`

    Args:
        user (str, optional): Username. Defaults to "User 1".
        inside_wsl (bool, optional): WSL only - access files installed inside WSL. Defaults to False.
    """

    base: Path
    user: str

    def __init__(self, user: str = "User 1", inside_wsl: bool = False):
        self.base = ""
        self.user = user

        if sys.platform == "darwin":
            "macOS"

            self.base = Path(os.environ["HOME"], ".local", "share")
        elif "win" in sys.platform:
            "Windows"

            self.base = Path(os.environ["APPDATA"])
        elif not inside_wsl and "microsoft" in Path("/proc/version").read_text():
            "WSL on Linux"

            drive, *winpath = (
                subprocess.check_output(["cmd.exe", "/c", "echo", "%APPDATA%"])
                .decode()
                .strip()
                .split("\\")
            )
            self.base = Path("/mnt", drive.split(":")[0].lower(), *winpath)
        else:
            "Linux"

            self.base = Path(os.environ["HOME"], ".local", "share")

    @property
    def path(self):
        """Returns Anki folder

        Returns:
            Path: Anki folder
        """

        return self.base.joinpath("Anki2", self.user)

    def show(self):
        """Open the folder in OS-specific file viewer"""

        opener = {"win32": "explorer.exe", "darwin": "open", "linux": "xdg-open"}[
            sys.platform
        ]

        subprocess.call([opener, str(self.path)])

    @property
    def collection(self):
        """Get User's `collection.anki2`

        Returns:
            Path: Path to `collection.anki2`
        """

        return self.base.joinpath("Anki2", self.user, "collection.anki2")

    def __repr__(self):
        return str(self.path)
