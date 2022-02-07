from ankisync2 import AnkiDesktop

from common.vocab import has_vocabs


if __name__ == "__main__":
    anki = AnkiDesktop(filename="collection.anki2")

    print(has_vocabs(anki))

    anki.close()
