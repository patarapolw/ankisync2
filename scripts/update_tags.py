import pprint
import shutil

# pylint: disable=import-error
from ankisync2.anki21 import db
from ankisync2.dir import get_anki_collection
from ankisync2.ankiconnect import ankiconnect


if __name__ == "__main__":
    shutil.copy(get_anki_collection("User 1"), "collection.anki2")
    db.database.init("collection.anki2")

    updates = {}

    for c in (
        db.Cards.select()
        .join(db.Decks)
        .switch(db.Cards)
        .join(db.Notes)
        .join(db.Notetypes)
        .where(db.Notetypes.name.collate("BINARY") == "zhlevel_vocab")
    ):
        updates.setdefault(c.did.name, set())
        updates[c.did.name].add(c.nid.id)

    for k, v in updates.items():
        ds = set(k.split("\x1f"))
        tags = ["zhlevel"]

        ankiconnect("addTags", notes=list(v), tags=tags)
