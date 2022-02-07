from ankisync2 import AnkiDesktop, ankiconnect


if __name__ == "__main__":
    # AnkiDesktop.backup("collection.anki2")
    anki = AnkiDesktop(filename="collection.anki2")

    updates = {}

    for c in (
        anki.db.Cards.select()
        .join(anki.db.Notes)
        .switch(anki.db.Cards)
        .join(anki.db.Decks)
        .where(anki.db.Decks.name.collate("NOCASE") ** "zhlevel\x1fvocab\x1f%")
    ):
        *tags, level, type_ = c.did.name.split("\x1f")
        tags.append(f"{type_}_{level.replace(' ', '_')}")

        for t in tags:
            updates.setdefault(t, set()).add(c.nid.id)

    for t, notes in updates.items():
        ankiconnect("addTags", notes=list(notes), tags=t)
