import pprint

# pylint: disable=import-error
from ankisync2.anki21 import db
from ankisync2.dir import AnkiPath


if __name__ == "__main__":
    db.database.init(AnkiPath().collection)

    """
    This `.collate("BINARY") is required to overcome a custom collation, unicase.`
    """
    nt = db.Notetypes.get(db.Notetypes.name.collate("BINARY") == "zhlevel_vocab")
    print(nt.id)
    print(nt.name)

    pp = pprint.PrettyPrinter()

    """
    Config is in Binary. Modify it at your risk.
    `.encode('utf-8')` doesn't work.
    """
    pp.pprint(nt.config)

    keys = [
        f.name
        for f in sorted(
            db.Fields.select(db.Fields.ord, db.Fields.name)
            .join(db.Notetypes)
            .where(db.Notetypes.name.collate("BINARY") == "zhlevel_vocab"),
            key=lambda f: f.ord,
        )
    ]

    pp.pprint(tuple(enumerate(keys)))

    # pp.pprint(
    #     [
    #         dict(zip(keys, n.flds))
    #         for n in db.Notes.select()
    #         .join(db.Notetypes)
    #         .where(db.Notetypes.name.collate("BINARY") == "zhlevel_vocab")
    #         .limit(10)
    #     ]
    # )
