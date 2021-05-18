from pathlib import Path
from typing import Union

from playhouse.shortcuts import model_to_dict

from . import db, builder


class Anki20:
    """Reads the original *.anki2 SQLite database

    Mutates the database to make it easier to read.
    """

    def __init__(self, filename: Union[str, Path], **kwargs):
        db.database.init(str(filename), **kwargs)

        if "col" not in db.database.get_tables():
            db.database.create_tables(
                [db.Col, db.Notes, db.Cards, db.Graves, db.Revlog]
            )
            db.Col.create()

        if "decks" not in db.database.get_tables():
            db.database.create_tables([db.Decks, db.Models, db.Templates])
            self.fix()

    def __iter__(self):
        """Iterates through Cards, with appropriate table joinings

        Yields:
            dict: Cards with deck. note content and model content
        """

        for c in (
            db.Cards.select(db.Cards, db.Decks, db.Notes, db.Models)
            .join(
                db.Decks, on=(db.Decks.id == db.Cards.did)  # pylint: disable=no-member
            )
            .switch(db.Cards)
            .join(
                db.Notes, on=(db.Notes.id == db.Cards.nid)  # pylint: disable=no-member
            )
            .join(
                db.Models,
                on=(db.Models.id == db.Notes.mid),  # pylint: disable=no-member
            )
        ):
            yield model_to_dict(c, backrefs=True)

    def fix(self):
        """Create the required tables for easy and fast manipulation"""

        c = db.Col.get()

        for d in c.decks.values():
            db.Decks.create(id=d["id"], name=d["name"])

        for m in c.models.values():
            db.Models.create(
                id=m["id"],
                name=m["name"],
                flds=[f["name"] for f in m["flds"]],
                css=m["css"],
            )

            for t in m["tmpls"]:
                db.Templates.create(
                    mid=m["id"], name=t["name"], qfmt=t["qfmt"], afmt=t["afmt"]
                )

    def finalize(self):
        """Remove the generated tables, for importing to the Anki app

        If you are using Apkg constructor, use `.export(filename)` instead.
        """

        c, _ = db.Col.get_or_create()
        decks = c.decks

        for d in db.Decks.select():
            decks[str(d.id)] = builder.Deck(id=d.id, name=d.name)

        models = c.models

        for m in db.Models.select():
            models[str(m.id)] = builder.Model(
                id=m.id,
                name=m.name,
                flds=[builder.Field(name=f, ord=i) for i, f in enumerate(m.flds)],
                tmpls=[
                    builder.Template(name=t.name, qfmt=t.qfmt, afmt=t.afmt, ord=i)
                    for i, t in enumerate(
                        db.Templates.select().where(
                            db.Templates.mid == m.id  # pylint: disable=no-member
                        )
                    )
                ],
            )

        c.decks = decks
        c.models = models
        c.save()

        db.database.drop_tables([db.Decks, db.Models, db.Templates])

    def close(self):
        """Close the database

        Equivalent to `db.database.close()`
        """

        db.database.close()