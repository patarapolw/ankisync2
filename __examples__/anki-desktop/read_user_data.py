import pprint

from ankisync2 import AnkiDesktop


if __name__ == "__main__":
    anki = AnkiDesktop()

    """
    This `.collate("BINARY") is required to overcome a custom collation, unicase.`
    """
    nt = anki.db.Notetypes.get(
        anki.db.Notetypes.name.collate("BINARY") == "zhlevel_vocab"
    )
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
            anki.db.Fields.select(anki.db.Fields.ord, anki.db.Fields.name)
            .join(anki.db.Notetypes)
            .where(anki.db.Notetypes.name.collate("BINARY") == "zhlevel_vocab"),
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
