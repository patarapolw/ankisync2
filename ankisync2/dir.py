import os


def get_anki_path(user: str) -> str:
    """
    Most reliable way is to go to
    Tools >> Add-ons >> View Files
    """

    if os.name == "posix":
        "Linux or macOS"

        return os.path.join(os.environ["HOME"], ".local", "share", "Anki2", user)
    else:
        "Windows"

        return os.path.join(os.environ["APPDATA"], "Anki2", user)


def get_anki_collection(user: str) -> str:
    """
    Get User's `collection.anki2`
    """

    return os.path.join(get_anki_path(user), "collection.anki2")
