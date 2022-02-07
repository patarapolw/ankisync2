from ankisync2.anki21 import db

from ankisync2.ankiconnect import ankiconnect


if __name__ == "__main__":
    # shutil.copy(AnkiPath().collection, "collection.anki2")
    db.database.init("collection.anki2")

    updates = {}

    for c in (
        db.Cards.select()
        .join(db.Notes)
        .switch(db.Cards)
        .join(db.Decks)
        .where(db.Decks.name.collate("NOCASE") ** "zhlevel\x1fvocab\x1f%")
    ):
        *tags, level, type_ = c.did.name.split("\x1f")
        tags.append(f"{type_}_{level.replace(' ', '_')}")

        for t in tags:
            updates.setdefault(t, set()).add(c.nid.id)

    for t, notes in updates.items():
        ankiconnect("addTags", notes=list(notes), tags=t)
