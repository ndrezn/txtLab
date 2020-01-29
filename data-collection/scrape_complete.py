from mwclient import Site
import mwparserfromhell as mw
import os
import requests
from lxml import html
from time import mktime
from datetime import datetime
import timeit
import asyncio
import aiohttp
import json


# class to track data about each change of a page
class Change:
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

    def __init__(
        self,
        index,
        title,
        time,
        revid,
        kind,
        user,
        comment,
        rating,
        content,
        added,
        removed,
    ):
        self.index = index
        self.title = title
        self.time = time
        self.revid = revid
        self.kind = kind
        self.user = user
        self.comment = comment
        self.rating = rating
        self.content = content
        self.added = added
        self.removed = removed


# class to track rating of a page and time of that rating
class Rating:
    # classification of article
    rating = ""
    # time of classification
    timestamp = 0

    def __init__(self, rating, timestamp):
        self.rating = rating
        self.timestamp = timestamp


# compare two strings
# input: two strings
def changes(cur, prev):
    a = []

    for word in prev:
        if word not in cur:
            a.append(word)

    return a


# pull users, handles hidden user errors
# input: sheet of metadata from mwclient
def get_users(metadata):
    users = []
    for rev in metadata:
        try:
            users.append(rev["user"])
        except (KeyError):
            users.append("hiddenuser")
    return users


# pull edit types (minor or not), handles untagged edits
# input: sheet of metadata from mwclient
def get_kind(metadata):
    kind = []
    for rev in metadata:
        if "minor" in rev:
            kind.append(1)
        else:
            kind.append(0)
    return kind


# check for comments
# input: sheet of metadata from mwclient
def get_comment(metadata):
    comment = []
    for rev in metadata:
        try:
            comment.append(rev["comment"])
        except (KeyError):
            comment.append("")
    return comment


# output classes of a page to a list (FA, good, etc.) given a talk page
# input: set of talk pages from metadata
def get_ratings(talk):
    timestamps = [rev["timestamp"] for rev in talk.revisions()]
    ratings = []
    content = []

    for cur in talk.revisions(prop="content"):
        if cur.__len__() is 1:
            content.append(prev)
        else:
            content.append(cur)

        prev = cur

    i = 0
    for version in content:
        try:
            templates = mw.parse(version.get("*")).filter_templates()
        except IndexError:
            continue

        rate = "NA"
        for template in templates:
            try:
                rate = template.get("class").value
                break
            except ValueError:
                continue

        rating = Rating(rate, datetime.fromtimestamp(mktime(timestamps[i])))

        ratings.append(rating)
        i += 1

    return ratings


# pull plain text representation of a revision from API
# input: revision id of a page, 0 (initial attempt at pulling the page)
async def get_text(revid, attempts):
    try:
        # async implementation of requests get
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://wikipedia.org/w/api.php",
                params={"action": "parse", "format": "json", "oldid": revid,},
            ) as resp:
                response = await resp.json()
    # request errors from server
    except:
        if attempts is 10:
            return -1
        # if there's a server error, just re-send the request until the server complies
        return await get_text(revid, attempts + 1)
    # check if page was deleted (deleted pages have no text and are therefore un-parsable)
    try:
        raw_html = response["parse"]["text"]["*"]
    except KeyError:
        return -1
    # parse raw html from response
    document = html.document_fromstring(raw_html)
    text = document.xpath("//p")
    paragraphs = []
    for paragraph in text:
        paragraphs.append(paragraph.text_content())

    cur = "".join(paragraphs)

    return cur


# overall function
# input: output path, page title
async def compare_edits(path, title):
    # prep
    site = Site("en.wikipedia.org")
    page = site.pages[title]
    talk = site.pages["Talk:" + title]
    ratings = get_ratings(talk)

    # collect metadata information
    metadata = [rev for rev in page.revisions()]
    users = get_users(metadata)
    kind = get_kind(metadata)
    comments = get_comment(metadata)

    revids = []
    history = []

    # collect list of revision ids
    for i in range(0, metadata.__len__()):
        revids.append(metadata[i]["revid"])

    texts = []

    # gather body content of all revisions (asynchronously)
    sema = 100
    for i in range(0, metadata.__len__(), +sema):
        texts += await asyncio.gather(
            *(get_text(revid, 0) for revid in revids[i : (i + sema)])
        )

    # texts = await asyncio.gather(*(get_text(revid, 0) for revid in revids))

    prev = ""

    j = 0

    for i in range(metadata.__len__() - 1, -1, -1):
        # skip deleted pages
        if texts[i] is -1:
            j += 1
            continue

        # iterate against talk page editions
        time = datetime.fromtimestamp(mktime(metadata[i]["timestamp"]))
        rating = "NA"
        for item in ratings:
            if time > item.timestamp:
                rating = item.rating
                break

        cur = texts[i].split()

        change = Change(
            i,
            title,
            time,
            metadata[i]["revid"],
            kind[i],
            users[i],
            comments[i],
            rating,
            texts[i],
            changes(prev, cur),
            changes(cur, prev),
        )

        # big json
        history += make_json(change)

        prev = cur

    print("Skipped pages:", j)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + title + ".json", "w") as outfile:
        json.dump(history, outfile)


# output metadata of a page to a text file
# input: output path, change object
def write_change(path, change):
    if not os.path.exists(path):
        os.makedirs(path)

    body = (
        str(change.revid)
        + " +++$+++ "
        + str(change.time)
        + " +++$+++ "
        + str(change.kind)
        + " +++$+++ "
        + str(change.user)
        + " +++$+++ "
        + str(change.comment)
        + " +++$+++ "
        + str(change.rating)
        + " +++$+++ "
    )

    with open(path + str(change.index) + ".txt", "w") as f:
        f.write(body)
        for item in change.added:
            f.write(item + " ")
        f.write(" +++$+++ ")
        for item in change.removed:
            f.write(item + " ")
        f.write(" +++$+++ " + change.content)


# convert change object into json data type
# input: change object
def make_json(change):
    body = [
        {
            "index": change.index,
            "metadata": {
                "revid": change.revid,
                "time": str(change.time),
                "kind": str(change.kind),
                "user": str(change.user),
                "comment": str(change.comment),
                "rating": str(change.rating),
            },
            "text": {
                "added": change.added,
                "removed": change.removed,
                "text": change.content,
            },
        }
    ]
    return body


def main():

    titles = ["Serpentwithfeet", "Charles Bradley (singer)"]

    for i in range(0, titles.__len__()):
        print(titles[i])
        path = "/Volumes/KINGSTON/txtlab/jsons/other_sample/"

        start = timeit.default_timer()

        asyncio.run(compare_edits(path, titles[i]))

        stop = timeit.default_timer()
        print("Time:", stop - start)

    # title = "Charles Bradley (singer)"
    # path = "/Users/nathandrezner/OneDrive - McGill University/McGill/" \
    # 	   "txt Lab/out/edit_compare/other/"
    #
    # start = timeit.default_timer()
    #
    # asyncio.run(compare_edits(path, title))
    #
    # stop = timeit.default_timer()
    # print('Time:', stop - start)


main()
