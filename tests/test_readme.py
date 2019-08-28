from ankisync2.anki import Apkg
from ankisync2 import db


def test_create():
    apkg = Apkg("example")  # Create example folder

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

    apkg.add_media("/Users/patarapolw/Desktop/Screen Shot 2019-08-28 at 12.10.52.png")

    apkg.zip(output="example1.apkg")
    apkg.close()
