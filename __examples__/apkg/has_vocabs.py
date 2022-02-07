import shutil
from typing import List

from ankisync2.dir import AnkiPath
from ankisync2.anki21 import db


def has_vocabs() -> List[str]:
    return [
        n.flds[0]
        for n in (
            db.Notes.select()
            .join(db.Notetypes)
            .where((db.Notetypes.name.collate("NOCASE") == "zhlevel_vocab"))
        )
    ]


if __name__ == "__main__":
    shutil.copy(AnkiPath().collection, "collection.anki2")
    db.database.init("collection.anki2")

    print(has_vocabs())

    db.database.close()
