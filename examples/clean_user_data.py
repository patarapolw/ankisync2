import pprint

# pylint: disable=import-error
from ankisync2.anki21 import db
from ankisync2.dir import get_anki_collection


if __name__ == "__main__":
    db.database.init(get_anki_collection("User 1"))

    pp = pprint.PrettyPrinter()

    f_ord = (
        db.Fields.select(db.Fields.ord, db.Fields.name)
        .join(db.Notetypes)
        .where(
            db.Notetypes.name.collate("BINARY") == "zhlevel_vocab"
            and db.Fields.name.collate("BINARY") == "traditional"
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
        db.Notes.select(db.Notes.id, db.Notes.flds)
        .join(db.Notetypes, on=(db.Notes.mid == db.Notetypes.id))
        .where(db.Notetypes.name.collate("BINARY") == "zhlevel_vocab")
    ):
        if list_get(n.flds, f_ord) == "None":
            flds = list(n.flds)
            flds[f_ord] = ""
            n.flds = flds
            updates.append(n)

    if len(updates):
        db.Notes.bulk_update(updates, fields=[db.Notes.flds])

    pp.pprint(
        [
            f[0]
            for f in (
                (n.id, list_get(n.flds, f_ord))
                for n in db.Notes.select(db.Notes.id, db.Notes.flds)
                .join(db.Notetypes, on=(db.Notes.mid == db.Notetypes.id))
                .where(db.Notetypes.name.collate("BINARY") == "zhlevel_vocab")
            )
            if f[1] is None
        ]
    )
