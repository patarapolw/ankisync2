# AnkiSync 2 (With doc examples auto-generator!)

[![PyPI version shields.io](https://img.shields.io/pypi/v/ankisync2.svg)](https://pypi.python.org/pypi/ankisync2/)
[![PyPI license](https://img.shields.io/pypi/l/ankisync2.svg)](https://pypi.python.org/pypi/ankisync2/)

\*.apkg and \*.anki2 file structure is very simple, but with some quirks of incompleteness.

[\*.apkg file structure](https://github.com/ankidroid/Anki-Android/wiki/Database-Structure) is a zip of at least two files.

```
.
├── example
│   ├── collection.anki2
│   ├── collection.anki21 # newer Anki Desktop creates and uses this file instead, while retaining the old one as stub.
│   ├── media # JSON of dict[int, str]
│   ├── 1  # Media files with the names masked as integers
│   ├── 2
│   ├── 3
|   └── ...
└── example.apkg
```

\*.anki2 is a SQLite file with foreign key disabled, and the usage of [some JSON schemas](/ankisync2/anki20/builder.py) instead of [some tables](/ankisync2/anki20/db.py#L51)

Also, \*.anki2 is used internally at [`os.path.join(appdirs.user_data_dir('Anki2'), 'User 1', 'collection.anki2')`](/ankisync2/dir.py#L75), so editing the SQLite there will also edit the database.

However, [internal \*.anki2 has recently changed](https://github.com/patarapolw/ankisync2/issues/3). If you need to edit internally, if maybe safer to do in Anki<=2.1.26. If you have trouble running two Anki versions (latest and 2.1.26), see [`/__utils__/anki2.1.26`](https://github.com/patarapolw/ankisync/tree/master/__utils__/anki2.1.26).

The `media` file is a text file of at least a string of `{}`, which is actually a dictionary of keys -- stringified int; and values -- filenames.

## Usage

Some [extra tables](/ankisync2/anki20/db.py#L51) are created if not exists.

```python
from ankisync2 import Apkg

with Apkg("example.apkg") as apkg:
    # Or Apkg("example/") also works - the folder named 'example' will be created.
    apkg.db.database.execute_sql(SQL, PARAMS)
    apkg.zip(output="example1.apkg")
```

I also support adding media.

```python
apkg.add_media("path/to/media.jpg")
```

To find the wanted cards and media, iterate though the `Apkg` and `Apkg.iter_media` object.

```python
for card in apkg:
    print(card)
```

## Creating a new \*.apkg

You can create a new \*.apkg via `Apkg` with any custom filename (and \*.anki2 via `Anki2()`). A folder required to create \*.apkg needs to be created first.

```python
apkg = Apkg("example")  # Create example folder
```

After that, the Apkg will require at least 1 card, which is connected to at least 1 note, 1 model, 1 template, and 1 deck; which should be created in this order.

1. Model, Deck
2. Template, Note
3. Card

```python
with Apkg("example.apkg") as apkg:
    m = apkg.db.Models.create(name="foo", flds=["field1", "field2"])
    d = apkg.db.Decks.create(name="bar::baz")
    t = [
        apkg.db.Templates.create(name="fwd", mid=m.id, qfmt="{{field1}}", afmt="{{field2}}"),
        apkg.db.Templates.create(name="bwd", mid=m.id, qfmt="{{field2}}", afmt="{{field1}}")
    ]
    n = apkg.db.Notes.create(mid=m.id, flds=["data1", "<img src='media.jpg'>"], tags=["tag1", "tag2"])
    c = [
        apkg.db.Cards.create(nid=n.id, did=d.id, ord=i)
        for i, _ in enumerate(t)
    ]
```

You can also add media, which is not related to the SQLite database.

```python
apkg.add_media("path/to/media.jpg")
```

Finally, finalize with

```python
apkg.export("example1.apkg")
```

## Updating an \*.apkg

This is also possible, by modifying `db.Notes.data` as `sqlite_ext.JSONField`, with `peewee.signals`.

It is now as simple as,

```python
with Apkg("example1.apkg") as apkg:
    for n in apkg.db.Notes.filter(db.Notes.data["field1"] == "data1"):
        n.data["field3"] = "data2"
        n.save()

    apkg.close()
```

## JSON schema of `Col.models`, `Col.decks`, `Col.conf` and `Col.dconf`

I have created `dataclasses` for this at [/ankisync2/builder.py](/ankisync2/builder.py). To serialize it, use `dataclasses.asdict` or

```python
from ankisync2 import DataclassJSONEncoder
import json

json.dumps(dataclassObject, cls=DataclassJSONEncoder)
```

## Editing user's `collection.anki2`

This can be found at `${ankiPath}/${user}/collection.anki2`. Of course, do this at your own risk. Always backup first.

```python
from ankisync2 import AnkiDesktop

AnkiDesktop.backup("/path/to/anki-desktop.db")
anki = AnkiDesktop(filename="/path/to/anki-desktop.db")
... # Edit as you please
AnkiDesktop.restore("/path/to/anki-desktop.db")
```

## Using `peewee` framework

This is based on `peewee` ORM framework. You can use Dataclasses and Lists directly, without converting them to string first.

## Examples

Please see [`/__examples__`](/__examples__), and [/tests](/tests).

## Installation

```bash
pip install ankisync2
```

# Related projects

- <https://github.com/patarapolw/ankisync>
- <https://github.com/patarapolw/AnkiTools>
