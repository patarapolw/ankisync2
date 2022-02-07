import pprint

from ankisync2 import AnkiDesktop


if __name__ == "__main__":
    anki = AnkiDesktop()

    pp = pprint.PrettyPrinter()

    f_ord = (
        anki.db.Fields.select(anki.db.Fields.ord, anki.db.Fields.name)
        .join(anki.db.Notetypes)
        .where(
            anki.db.Notetypes.name.collate("BINARY") == "zhlevel_vocab"
            and anki.db.Fields.name.collate("BINARY") == "traditional"
        )
        .first()
    ).ord

    def list_get(ls, i):
        try:
            return ls[i]
        except IndexError:
            pass

    updates = []

    for n in (
        anki.db.Notes.select(anki.db.Notes.id, anki.db.Notes.flds)
        .join(anki.db.Notetypes)
        .where(anki.db.Notetypes.name.collate("BINARY") == "zhlevel_vocab")
    ):
        if list_get(n.flds, f_ord) == "None":
            flds = list(n.flds)
            flds[f_ord] = ""
            n.flds = flds
            updates.append(n)

    if len(updates):
        anki.db.Notes.bulk_update(updates, fields=[anki.db.Notes.flds])

    pp.pprint(
        [
            f[0]
            for f in (
                (n.id, list_get(n.flds, f_ord))
                for n in anki.db.Notes.select(anki.db.Notes.id, anki.db.Notes.flds)
                .join(anki.db.Notetypes)
                .where(anki.db.Notetypes.name.collate("BINARY") == "zhlevel_vocab")
            )
            if f[1] is None
        ]
    )
