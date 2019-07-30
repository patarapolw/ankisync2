# AnkiSync 2

\*.apkg and \*.anki2 file structure is very simple, but with some quirks of incompleteness.

[\*.apkg file structure](https://github.com/ankidroid/Anki-Android/wiki/Database-Structure) is a zip of at least two files.

```
.
├── example
│   ├── example.anki2
│   ├── media
│   ├── 1  # Media files with the names masked as numbers
│   ├── 2
│   ├── 3
|   └── ...
└── example.apkg
```

\*.anki2 is a SQLite file with foreign key disabled, and the usage of [some JSON schemas](/ankisync2/builder.py) instead of [some tables](/ankisync2/db.py#L46)

Also, \*.anki2 is used internally at [`os.path.join(appdirs.user_data_dir('Anki2'), 'User 1', 'collection.anki2')`](https://github.com/patarapolw/ankisync/blob/master/ankisync/dir.py#L9), so editing the SQLite there will also edit the database.

The `media` file is a text file of at least a string of `{}`, which is actually a dictionary of keys -- stringified int; and values -- filenames.

## Usage

Some [extra tables](/ankisync2/db.py#L46) are created if not exists.

```python
from ankisync2.anki import Anki2, Apkg
apkg = Apkg("example.apkg")  # Or Apkg("example/") also works, otherwise the folder named 'example' will be created.
apkg.db.execute_sql(SQL, PARAMS)
apkg.zip(output="example1.apkg")
```

I also support adding media.

```python
apkg.add_media("media.jpg")
```

To find the wanted cards and media, iterate though the `Apkg` and `Apkg.iter_media` object.

```python
iter_apkg = iter(apkg)
for i in range(5):
    print(next(iter_apkg))
```

## Creating a new *.apkg

You can create a new \*.apkg via `Apkg` with any custom filename (and \*.anki2 via `Anki2()`). A folder required to create \*.apkg needs to be created first.

```python
from ankisync2.anki import Apkg
apkg = Apkg("example")  # Create example folder
```

After that, the Apkg will require at least 1 card, which is connected to at least 1 note, 1 model, 1 template, and 1 deck; which should be created in this order.

1. Model, Deck
2. Template, Note
3. Card

```python
from ankisync2 import db
m = db.Models.create(name="foo", flds=["field1", "field2"])
d = db.Decks.create(name="bar::baz")
t = [
    db.Templates.create(name="fwd", mid=m.id, qfmt="{{field1}}", afmt="{{field2}}"),
    db.Templates.create(name="bwd", mid=m.id, qfmt="{{field2}}", afmt="{{field1}}")   
]
n = db.Notes.create(mid=m.id, flds=["data1", "<img src='media.jpg'>"], tags=["tag1", "tag2"])
c = [
    db.Cards.create(nid=n.id, did=d.id, ord=i)
    for i, _ in enumerate(t)
]
```

You can also add media, which is not related to the SQLite database.

```python
apkg.add_media("media.jpg")
```

Finally, finalize with

```python
apkg.zip(output="example1.apkg")
```

## JSON schema of `Col.models`, `Col.decks`, `Col.conf` and `Col.dconf`

I have created `dataclasses` for this at [/ankisync2/builder.py](/ankisync2/builder.py). To serialize it, use `dataclasses.asdict` or

```python
from ankisync2.util import DataclassJSONEncoder
import json
json.dumps(dataclassObject, cls=DataclassJSONEncoder)
```

For an example of how this works, please see [/ankisync2/anki.py#L56](/ankisync2/anki.py#L56)

## Using `peewee` framework

You can also use `peewee` ORM framework; and [ArrayField](/ankisync2/db.py#L21), [X1fField](/ankisync2/db.py#L31) and [JSONField](/ankisync2/db.py#L31) will be automated. You can use Dataclasses and Lists directly, without converting them to string first.

## Examples

Please see [/example.ipynb](/example.ipynb).

## Installation

```bash
pip install ankisync2
```

# Related projects

- <https://github.com/patarapolw/ankisync>
- <https://github.com/patarapolw/AnkiTools>
