import sqlite3
import sys
from typing import Dict

from ankisync2.anki21 import db  # pylint: disable=import-error
from ankisync2.ankiconnect import ankiconnect  # pylint: disable=import-error
from scripts.has_vocabs import has_vocabs  # pylint: disable=import-error


def create_note(simplified: str, deckName: str = "Default"):
    create_notes({simplified: deckName})


def create_notes(cards: Dict[str, str]):
    db.database.init("collection.anki2")
    existing_vocab = set(has_vocabs())
    db.database.close()

    cedict = sqlite3.connect("C:\\Users\\Pacharapol W\\Dropbox\\database\\cedict.db")
    cedict.row_factory = sqlite3.Row

    tatoeba = sqlite3.connect("C:\\Users\\Pacharapol W\\Dropbox\\database\\tatoeba.db")
    tatoeba.row_factory = sqlite3.Row

    rs = cedict.execute(
        f"""
    SELECT
        simplified,
        GROUP_CONCAT(traditional, ' | ')    traditional,
        GROUP_CONCAT(pinyin, ' | ')         pinyin,
        GROUP_CONCAT(english, ' | ')        english
    FROM vocab
    WHERE
        simplified NOT IN ({",".join("?" for _ in enumerate(existing_vocab))}) AND
        simplified IN ({",".join("?" for _ in cards.keys())})
    GROUP BY simplified
    """,
        (*existing_vocab, *cards.keys()),
    )

    for r in rs:
        sentence = ""

        ts = tatoeba.execute(
            """
        SELECT
            a.[text]                    chinese,
            GROUP_CONCAT(b.[text], '; ') english
        FROM        sentence    a
        INNER JOIN  translation t ON a.id == t.sentence_id
        INNER JOIN  sentence    b ON b.id == t.translation_id
        WHERE
            a.[text] LIKE '%'||?||'%' AND
            a.lang = 'cmn' AND
            b.lang = 'eng'
        GROUP BY a.[text]
        LIMIT 10
        """,
            (r["simplified"],),
        ).fetchall()

        if len(ts):
            sentence += "<ul>"

            for t in ts:
                sentence += f'<li>{t["chinese"]} {t["english"]}</li>'

            sentence += "</ul>"

        existing = ankiconnect(
            "findCards", query=f"\"simplified:{r['simplified']}\" note:zhlevel\\_vocab"
        )
        if len(existing):
            ankiconnect("changeDeck", cards=existing, deck=cards[r["simplified"]])
        else:
            ankiconnect(
                "addNote",
                note={
                    "deckName": cards[r["simplified"]],
                    "modelName": "zhlevel_vocab",
                    "fields": {
                        "simplified": r["simplified"],
                        "english": r["english"],
                        "traditional": r["traditional"] or "",
                        "pinyin": r["pinyin"],
                        "sentences": sentence,
                    },
                },
            )


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    create_note(*sys.argv[1:])
