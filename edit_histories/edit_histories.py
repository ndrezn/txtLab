from mwclient import Site
import mwparserfromhell as mw
import os
import requests
from lxml import html
from time import mktime
from datetime import datetime
import time


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

    def __init__(self, index, title, time, revid, kind, user, comment, rating, content, added, removed):
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
    rating = ''
    # time of classification
    timestamp = 0

    def __init__(self, rating, timestamp):
        self.rating = rating
        self.timestamp = timestamp


# compare two strings
def changes(cur, prev):
    a = []

    for word in prev:
        if word not in cur:
            a.append(word)

    return a


# pull plain text representation of a revision from API
def get_text(id):
    response = requests.get(
        "https://wikipedia.org/w/api.php",
        params={
            "action": "parse",
            'format': 'json',
            'oldid' : id,
        }
    ).json()

    raw_html = response['parse']['text']['*']
    document = html.document_fromstring(raw_html)
    text = document.xpath('//p')
    paragraphs = []

    for paragraph in text:
        paragraphs.append(paragraph.text_content().encode('utf-8'))

    return "".join(paragraphs)


# pull users, handles hidden user errors
def get_users(metadata):
    users = []
    for rev in metadata:
        try:
            users.append(rev['user'])
        except(KeyError):
            users.append("hiddenuser")
    return users


# pull edit types (minor or not), handles untagged edits
def get_kind(metadata):
    kind = []
    for rev in metadata:
        if 'minor' in rev:
            kind.append(1)
        else:
            kind.append(0)
    return kind


# check for comments
def get_comment(metadata):
    comment = []
    for rev in metadata:
        try:
            comment.append(rev['comment'])
        except(KeyError):
            comment.append('')
    return comment


# output classes of a page to a text file (FA, good, etc.) given a talk page
def get_ratings(talk):
    timestamps = [rev['timestamp'] for rev in talk.revisions()]
    ratings = []
    content = []

    for cur in talk.revisions(prop='content'):
        if cur.__len__() is 1:
            content.append(prev)
        else:
            content.append(cur)

        prev = cur

    i = 0
    for version in content:
        templates = mw.parse(version.items()[2]).filter_templates()
        rate = 'NA'
        for template in templates:
            try:
                rate = template.get('class').value
                break
            except(ValueError):
                continue

        rating = Rating(rate, datetime.fromtimestamp(mktime(timestamps[i])))

        ratings.append(rating)
        i += 1

    return ratings


def compare_edits(title):
    site = Site('en.wikipedia.org')
    page = site.pages[title]
    talk = site.pages["Talk:" + title]
    ratings = get_ratings(talk)

    # collect metadata information
    metadata = [rev for rev in page.revisions()]
    users = get_users(metadata)
    kind = get_kind(metadata)
    comments = get_comment(metadata)

    # collect revision contents
    content = []

    for cur in page.revisions(prop='content'):
        if cur.__len__() is 1:
            content.append(prev)
        else:
            content.append(cur)

        prev = cur

    for i in range(0, metadata.__len__()):
        if i % 5 != 0:
            continue

        try:
            prev = get_text(metadata[i+5]['revid']).split()
        except(IndexError):
            prev = ""

        # iterate against talk page editions
        time = datetime.fromtimestamp(mktime(metadata[i]['timestamp']))
        rating = 'NA'
        for item in ratings:
            if time > item.timestamp:
                rating = item.rating
                break

        # Alternative method of capturing the body text of a revision:
        # Instead of parsing the HTML straight form the API, parse the markup using mwparserfromhell.
        # isolate the body text of the revision (cur.items()[2])
        # then, parse the body text with mw (mw.parse())
        # then, use mw to turn the markup text into plain text (.stripcode())
        # then, convert to a utf-8 string using .encode
        # text = mw.parse(content[i].items()[2]).strip_code().encode('utf-8')

        text = get_text(metadata[i]['revid'])

        cur = text.split()

        change = Change(i, title, time, metadata[i]['revid'], kind[i], users[i],
                        comments[i], rating, text, changes(prev, cur),
                        changes(cur, prev))

        write_change(change)


# output metadata of a page to a text file
def write_change(change):
    path = "/Users/nathandrezner/OneDrive - McGill University/McGill/txt Lab/" \
           "out/edit_compare/novels/" + change.title + "/"

    if not os.path.exists(path):
        os.makedirs(path)

    with open(path + str(change.index) + ".txt", 'w') as f:
        f.write(str(change.revid) + " +++$+++ " + str(change.time) + " +++$+++ " +
                str(change.kind) + " +++$+++ " + change.user.encode('utf-8') + " +++$+++ " +
                change.comment.encode('utf-8') + " +++$+++ " + change.rating.encode('utf-8') + " +++$+++ ")
        for item in change.added:
            f.write(item + " ")
        f.write(" +++$+++ ")
        for item in change.removed:
            f.write(item + " ")
        f.write(" +++$+++ " + change.content)


def main():
    f = open('/Users/nathandrezner/OneDrive - McGill University/McGill/'
             'txt Lab/out/edit_compare/lists/novels.txt', 'r')
    titles = [line.strip() for line in f.readlines()]

    for title in titles:
        print title
        compare_edits(title)


start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
