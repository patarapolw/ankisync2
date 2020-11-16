from pathlib import Path
from typing import Union
from zipfile import ZipFile
import json
import shutil
from playhouse.shortcuts import model_to_dict

from .anki20 import db, builder


class Anki2:
    def __init__(self, filename: Union[str, Path]):
        db.database.init(str(filename))

        if "col" not in db.database.get_tables():
            db.database.create_tables(
                [db.Col, db.Notes, db.Cards, db.Graves, db.Revlog]
            )
            db.Col.create()

        if "decks" not in db.database.get_tables():
            db.database.create_tables([db.Decks, db.Models, db.Templates])
            self.fix()

        for n in db.Notes.select(db.Notes.flds, db.Models).join(
            db.Models, on=(db.Models.id == db.Notes.mid)
        ):
            n.data = dict(zip(n.flds, n.model.flds))
            n.save()

    def __iter__(self):
        for c in (
            db.Cards.select(db.Cards, db.Decks, db.Notes, db.Models)
            .join(db.Decks, on=(db.Decks.id == db.Cards.did))
            .switch(db.Cards)
            .join(db.Notes, on=(db.Notes.id == db.Cards.nid))
            .join(db.Models, on=(db.Models.id == db.Notes.mid))
        ):
            yield model_to_dict(c, backrefs=True)

    @staticmethod
    def fix():
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
                        db.Templates.select().where(db.Templates.mid == m.id)
                    )
                ],
            )

        c.decks = decks
        c.models = models
        c.save()

        db.database.drop_tables([db.Decks, db.Models, db.Templates])
        for n in db.Notes.select():
            if n.data:
                n.data = ""
                n.save()


class Apkg(Anki2):
    original: Path
    folder: Path
    media_path: Path

    def __init__(self, filename_or_dir: Union[str, Path]):
        self.original = Path(filename_or_dir)
        if not self.original.is_dir():
            self.folder = self.original.with_suffix("")
            self.unzip()
        else:
            self.folder = self.original
        self.folder.mkdir(exist_ok=True)

        self.media_path = self.folder.joinpath("media")
        if not self.media_path.exists():
            self.media_path.write_text("{}")

        super().__init__(self.folder.joinpath("collection.anki2"))

    def unzip(self):
        if self.original.exists():
            with ZipFile(self.original) as zf:
                zf.extractall(self.folder)

    def zip(self, output: Union[str, Path]):
        with ZipFile(output, "w") as zf:
            for f in self.folder.iterdir():
                zf.write(str(f.resolve()), arcname=f.name)

    @property
    def media(self) -> dict:
        return json.loads(self.media_path.read_text())

    @media.setter
    def media(self, value: dict):
        with self.media_path.open("w") as f:
            json.dump(value, f)

    def iter_media(self):
        for k, v in self.media.items():
            yield {"path": k, "name": v}

    def add_media(self, file_path: Union[str, Path], archive_name: str = "") -> int:
        media = self.media
        file_id = max(int(i) for i in (0, *media.keys())) + 1

        if not archive_name:
            archive_name = Path(file_path).name

        if any(sep in archive_name for sep in {"/", "\\"}):
            raise ValueError("Media name does not support sub-folders")

        if str(file_path) != str(self.folder.joinpath(archive_name)):
            shutil.copy(str(file_path), str(self.folder.joinpath(archive_name)))

        media[str(file_id)] = archive_name

        self.media = media

        return file_id

    def close(self):
        self.finalize()
        shutil.rmtree(self.folder)
