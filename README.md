# AnkiSync 2

\*.apkg and \*.anki2 file structure is very simple, but with some quirks of incompleteness.

[\*.apkg file structure](https://github.com/ankidroid/Anki-Android/wiki/Database-Structure) is a zip of two files.

```
.
├── example
│   ├── example.anki2
│   └── media
└── example.apkg
```

\*.anki2 is a SQLite file with foreign key disabled, and the usage of [some JSON schemas](/ankisync2/builder/default.py) instead of [some tables](/ankisync2/db.py#L46)

Also, \*.anki2 is used internally at [`os.path.join(appdirs.user_data_dir('Anki2'), 'User 1', 'collection.anki2')`](https://github.com/patarapolw/ankisync/blob/master/ankisync/dir.py#L9), so editing the SQLite there will also edit the database.

## Usage

Some [extra tables](/ankisync2/db.py#L46) are created if not exists.

```python
from ankisync2.anki import Anki2, Apkg
apkg = Apkg("example.apkg")
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

## Examples

Please see [/example.ipynb](/example.ipynb).

## Installation

```bash
pip install ankisync2
```

# Related projects

- <https://github.com/patarapolw/ankisync>
- <https://github.com/patarapolw/AnkiTools>
