from ankisync2 import Apkg


def test_create():
    apkg = Apkg("example")  # Create example folder

    m = apkg.db.Models.create(name="foo", flds=["field1", "field2"])
    d = apkg.db.Decks.create(name="bar::baz")
    t = [
        apkg.db.Templates.create(
            name="fwd", mid=m.id, qfmt="{{field1}}", afmt="{{field2}}"
        ),
        apkg.db.Templates.create(
            name="bwd", mid=m.id, qfmt="{{field2}}", afmt="{{field1}}"
        ),
    ]
    n = apkg.db.Notes.create(
        mid=m.id, flds=["data1", "<img src='media.png'>"], tags=["tag1", "tag2"]
    )
    [apkg.db.Cards.create(nid=n.id, did=d.id, ord=i) for i, _ in enumerate(t)]

    apkg.add_media("media.png")

    apkg.export("example1.apkg")
    apkg.close()
