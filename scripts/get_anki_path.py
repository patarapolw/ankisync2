import os
import webbrowser

from appdirs import AppDirs


def get_anki_path(user: str):
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
    print(webbrowser.open(get_anki_path("User 1")))
