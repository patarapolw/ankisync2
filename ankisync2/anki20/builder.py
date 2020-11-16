import dataclasses as dc
from typing import List
from time import time


@dc.dataclass
class Conf:
    nextPos = 1
    estTimes = True
    activeDecks = [1]
    sortType = "noteFld"
    timeLim = 0
    sortBackwards = False
    addToCur = True
    curDeck = 1
    newBury = True
    newSpread = 0
    activeCols = ["noteFld", "template", "cardDue", "deck"]
    savedFilters = {}
    dueCounts = True
    curModel = 1540929274846
    collapseTime = 1200


@dc.dataclass
class Field:
    name: str
    ord: int
    size = 20
    media = []
    rtl = False
    font = "Arial"
    sticky = False


@dc.dataclass
class Template:
    qfmt: str
    afmt: str
    name: str
    ord: int
    did: int = None
    bqfmt = ""
    bafmt = ""


@dc.dataclass
class Model:
    id: int
    name: str
    flds: List[Field]
    tmpls: List[Template]
    vers = []
    tags = []
    did = 1
    usn = -1
    sortf = 0
    latexPre = "\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\begin{document}\n"
    latexPost = "\\end{document}"
    type = 1
    css = ".card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n"
    mod: int = dc.field(default_factory=lambda: int(time()))


@dc.dataclass
class Deck:
    id: int
    name: str
    conf = 1
    extendRev = 50
    extendNew = 10
    usn = 0
    collapsed = False
    newToday = [0, 0]
    timeToday = [0, 0]
    revToday = [0, 0]
    lrnToday = [0, 0]
    dyn = 0
    desc = ""
    mod: int = dc.field(default_factory=lambda: int(time()))


@dc.dataclass
class DConfLapse:
    leechFails = 8
    minInt = 1
    delays = [10]
    leechAction = 0
    mult = 0


@dc.dataclass
class DConfRev:
    perDay = 200
    ivlFct = 1
    maxIvl = 36500
    minSpace = 1
    ease4 = 1.3
    bury = False
    fuzz = 0.05


@dc.dataclass
class DConfNew:
    separate = True
    delays = [1, 10]
    perDay = 20
    ints = [1, 4, 7]
    initialFactor = 2500
    bury = False
    order = 1


@dc.dataclass
class DConf:
    id = 1
    name = "default"
    replayq = True
    lapse = DConfLapse()
    rev = DConfRev()
    new = DConfNew()
    timer = 0
    maxTaken = 60
    usn = 0
    autoplay = True
    mod: int = dc.field(default_factory=lambda: int(time()))
