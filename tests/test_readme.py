from ankisync2.apkg import Apkg, db


def test_create():
    apkg = Apkg("example")  # Create example folder

    m = db.Models.create(name="foo", flds=["field1", "field2"])
    d = db.Decks.create(name="bar::baz")
    t = [
        db.Templates.create(name="fwd", mid=m.id, qfmt="{{field1}}", afmt="{{field2}}"),
        db.Templates.create(name="bwd", mid=m.id, qfmt="{{field2}}", afmt="{{field1}}"),
    ]
    n = db.Notes.create(
        mid=m.id, flds=["data1", "<img src='media.png'>"], tags=["tag1", "tag2"]
    )
    [db.Cards.create(nid=n.id, did=d.id, ord=i) for i, _ in enumerate(t)]

    apkg.add_media("media.png")

    apkg.export("example1.apkg")
    apkg.close()
