from ankisync2 import AnkiDesktop

from common.notes import create_notes

if __name__ == "__main__":
    anki = AnkiDesktop(filename="collection.anki2")

    cards = dict(
        (c.note.flds[1].split("[")[0], c.deck.name.replace("\x1f", "::"))
        for c in anki.db.Cards.select()
        .join(anki.db.Decks)
        .where((anki.db.Decks.name.collate("NOCASE") ** "Chinese%"))
    )

    create_notes(anki, cards)

    anki.close()
