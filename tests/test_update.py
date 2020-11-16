from ankisync2.apkg import Apkg, db


def test_update():
    apkg = Apkg("example1.apkg")

    for n in db.Notes.filter(db.Notes.data["field1"] == "data1"):
        n.data["field3"] = "data2"
        n.save()

    apkg.close()
