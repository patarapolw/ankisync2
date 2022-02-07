from typing import Union
from pathlib import Path
import shutil

from .ankiconnect import ankiconnect
from .apkg import Apkg
from .dir import AnkiPath
from .util import DataclassJSONEncoder
from .anki20 import db, Anki20
from .anki21 import db as db_new

import semver

__all__ = [
    "ankiconnect",
    "Apkg",
    "Anki20",
    "Anki2",
    "AnkiDesktop",
    "AnkiPath",
    "DataclassJSONEncoder",
]

Anki2 = Anki20


class AnkiDesktop:
    def __init__(self, version: str = "2.1.49", filename: str = None) -> None:
        self.db = db_new if semver.compare(version, "2.1.26") >= 0 else db

        if filename is None:
            filename = AnkiPath().collection

        self.filename = filename
        self.version = version
        self.db.database.init(filename)

    @staticmethod
    def backup(target: Union[str, Path]):
        shutil.copy(AnkiPath().collection, target)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.db.database.close()
