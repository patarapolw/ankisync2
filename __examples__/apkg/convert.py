from ankisync2.anki21 import db
from common.notes import create_notes

if __name__ == "__main__":
    db.database.init("collection.anki2")

    cards = dict(
        (c.note.flds[1].split("[")[0], c.deck.name.replace("\x1f", "::"))
        for c in db.Cards.select()
        .join(db.Decks)
        .where((db.Decks.name.collate("NOCASE") ** "Chinese%"))
    )

    db.database.close()

    create_notes(cards)
