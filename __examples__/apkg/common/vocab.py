from typing import List

from ankisync2 import AnkiDesktop


def has_vocabs(anki: AnkiDesktop) -> List[str]:
    return [
        n.flds[0]
        for n in (
            anki.db.Notes.select()
            .join(anki.db.Notetypes)
            .where((anki.db.Notetypes.name.collate("NOCASE") == "zhlevel_vocab"))
        )
    ]
