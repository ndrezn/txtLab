## class to track data about each change of a page

import json
import os


class Page:
    # edit level
    index = 0
    # page title
    title = ""
    # time edit was made
    time = 0
    # id number of revision
    revid = 0
    # minor or non-minor edit
    kind = 0
    # user who made the edit
    user = ""
    # comment attached to the edit
    comment = ""
    # class of article (FA, Good, stub, etc.)
    rating = 0
    # content of the edit page
    content = ""
    # words added
    added = []
    # words removed
    removed = []

    def __init__(self, index, title, time, revid, kind, user, comment, rating, content):
        self.index = index
        self.title = title
        self.time = time
        self.revid = revid
        self.kind = kind
        self.user = user
        self.comment = comment
        self.rating = rating
        self.content = content


def read_json(file):

    with open(file, encoding="utf-8", errors="ignore") as json_data:
        d = json.load(json_data)

    s = os.path.basename(file)
    title, ext = os.path.splitext(s)

    revisions = []

    for item in d:
        index = item["index"]
        time = item["metadata"]["time"]
        revid = item["metadata"]["revid"]
        kind = item["metadata"]["kind"]
        user = item["metadata"]["user"]
        comment = item["metadata"]["comment"]
        rating = item["metadata"]["rating"]
        content = item["text"]["text"]
        page = Page(index, title, time, revid, kind, user, comment, rating, content)

        revisions.append(page)

    return revisions
