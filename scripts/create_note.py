import sqlite3
import sys

# pylint: disable=import-error
from ankisync2.ankiconnect import ankiconnect


def create_note(simplified: str):
    mid = ankiconnect("modelNamesAndIds")["zhlevel_vocab"]
    nids = ankiconnect("findNotes", query=f"mid:{mid}")

    existing_vocab = set(
        n["fields"]["simplified"]["value"] for n in ankiconnect("notesInfo", notes=nids)
    )

    cedict = sqlite3.connect("C:\\Users\\Pacharapol W\\Dropbox\\database\\cedict.db")
    cedict.row_factory = sqlite3.Row

    tatoeba = sqlite3.connect("C:\\Users\\Pacharapol W\\Dropbox\\database\\tatoeba.db")
    tatoeba.row_factory = sqlite3.Row

    r = cedict.execute(
        f"""
    SELECT
        simplified,
        GROUP_CONCAT(traditional, ' | ')    traditional,
        GROUP_CONCAT(pinyin, ' | ')         pinyin,
        GROUP_CONCAT(english, ' | ')        english
    FROM vocab
    WHERE
        simplified NOT IN ({",".join("?" for _ in enumerate(existing_vocab))}) AND
        simplified = ?
    GROUP BY simplified
    """,
        (*existing_vocab, simplified),
    ).fetchone()

    if r is None:
        return

    sentence = ""

    ts = tatoeba.execute(
        """
    SELECT
        a.[text]                    chinese,
        GROUP_CONCAT(b.[text], ';') english
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

    return ankiconnect(
        "addNote",
        note={
            "deckName": "Default",
            "modelName": "zhlevel_vocab",
            "fields": {
                "simplified": r["simplified"],
                "english": r["english"],
                "traditional": r["traditional"] or "",
                "pinyin": r["pinyin"],
                "sentence": sentence,
            },
        },
    )


if __name__ == "__main__":
    create_note(sys.argv[1])
