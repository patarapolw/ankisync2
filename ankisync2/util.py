from hashlib import sha1
import re
from html.entities import name2codepoint
import dataclasses, json


def checksum(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    return sha1(data).hexdigest()


def field_checksum(data):
    # 32 bit unsigned number from first 8 digits of sha1 hash
    return int(checksum(data)[:8], 16)


reComment = re.compile("(?s)<!--.*?-->")
reStyle = re.compile("(?si)<style.*?>.*?</style>")
reScript = re.compile("(?si)<script.*?>.*?</script>")
reTag = re.compile("(?s)<.*?>")
reEnts = re.compile(r"&#?\w+;")
reMedia = re.compile("(?i)<img[^>]+src=[\"']?([^\"'>]+)[\"']?[^>]*>")


def stripHTML(s):
    s = reComment.sub("", s)
    s = reStyle.sub("", s)
    s = reScript.sub("", s)
    s = reTag.sub("", s)
    s = entsToTxt(s)
    return s


def stripHTMLMedia(s):
    "Strip HTML but keep media filenames"
    s = reMedia.sub(" \\1 ", s)
    return stripHTML(s)


def minimizeHTML(s):
    "Correct Qt's verbose bold/underline/etc."
    s = re.sub('<span style="font-weight:600;">(.*?)</span>', "<b>\\1</b>", s)
    s = re.sub('<span style="font-style:italic;">(.*?)</span>', "<i>\\1</i>", s)
    s = re.sub(
        '<span style="text-decoration: underline;">(.*?)</span>', "<u>\\1</u>", s
    )
    return s


def htmlToTextLine(s):
    s = s.replace("<br>", " ")
    s = s.replace("<br />", " ")
    s = s.replace("<div>", " ")
    s = s.replace("\n", " ")
    s = re.sub(r"\[sound:[^]]+\]", "", s)
    s = re.sub(r"\[\[type:[^]]+\]\]", "", s)
    s = stripHTMLMedia(s)
    s = s.strip()
    return s


def entsToTxt(html):
    # entitydefs defines nbsp as \xa0 instead of a standard space, so we
    # replace it first
    html = html.replace("&nbsp;", " ")

    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return chr(int(text[3:-1], 16))
                else:
                    return chr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = chr(name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is

    return reEnts.sub(fixup, html)


def bodyClass(col, card):
    bodyclass = "card card%d" % (card.ord + 1)
    if col.conf.get("nightMode"):
        bodyclass += " nightMode"
    return bodyclass


class DataclassJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)
