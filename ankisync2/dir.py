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

    base: str
    user: str

    def __init__(self, user: str = "User 1", inside_wsl: bool = False):
        self.base = ""
        self.user = user

        if sys.platform == "darwin":
            "macOS"

            self.base = os.path.join(os.environ["HOME"], ".local", "share")
        elif "win" in sys.platform:
            "Windows"

            self.base = os.environ["APPDATA"]
        elif not inside_wsl and "microsoft" in Path("/proc/version").read_text():
            "WSL on Linux"

            drive, *winpath = (
                subprocess.check_output(["cmd.exe", "/c", "echo", "%APPDATA%"])
                .decode()
                .strip()
                .split("\\")
            )
            self.base = os.path.join("/mnt", drive.split(":")[0].lower(), *winpath)
        else:
            "Linux"

            self.base = os.path.join(os.environ["HOME"], ".local", "share")

    @property
    def path(self):
        """Returns Anki folder

        Returns:
            str: Anki folder
        """

        return os.path.join(self.base, "Anki2", self.user)

    def show(self):
        """Open the folder in OS-specific file viewer"""

        opener = {"win32": "explorer.exe", "darwin": "open", "linux": "xdg-open"}[
            sys.platform
        ]

        subprocess.call([opener, self.path])

    @property
    def collection(self):
        """Get User's `collection.anki2`

        Returns:
            str: Path to `collection.anki2`
        """

        return os.path.join(self.base, "Anki2", self.user, "collection.anki2")

    def __repr__(self):
        return self.path
