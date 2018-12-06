from mwclient import Site
import mwparserfromhell as mw
import os

class Change:
    editCount = 0
    index = 0
    title = ""
    revid = 0
    kind = 0
    user = ""
    comment = ""
    content = ""
    added = []
    removed = []

    def __init__(self, index, title, revid, kind, user, comment, content, added, removed):
        self.index = index
        self.title = title
        self.revid = revid
        self.kind = kind
        self.user = user
        self.comment = comment
        self.content = content
        self.added = added
        self.removed = removed
        Change.editCount += 1


# compare two strings
def added(cur, prev):
    a = []

    for word in prev:
        if word not in cur:
            a.append(word)

    return a


def get_users(metadata):
    users = []
    for rev in metadata:
        if 'user' in rev:
            users.append(rev['user'])
        else:
            users.append("hiddenuser")
    return users


def get_kind(metadata):
    kind = []
    for rev in metadata:
        if 'minor' in rev:
            kind.append(1)
        else:
            kind.append(0)
    return kind


def write_change(change):
    path = "/Users/nathandrezner/OneDrive - McGill University/McGill/txt Lab/" \
           "out/edit_compare/metadata/other/" + change.title + "/"
    if not os.path.exists(path):
        os.makedirs(path)

    with open(path + str(change.index) + ".txt", 'w') as f:
        f.write(str(change.revid) + "\n" + str(change.kind) + "\n" +
                change.user.encode('utf-8') + "\n" + change.comment.encode('utf-8') + "\n")
        for item in change.added:
            f.write(item + " ")
        f.write("\n")
        for item in change.removed:
            f.write(item + " ")


def write_content(change):
    path = "/Users/nathandrezner/OneDrive - McGill University/McGill/txt Lab/" \
           "out/edit_compare/content/other/" + change.title + "/"
    if not os.path.exists(path):
        os.makedirs(path)

    with open(path + str(change.index) + ".txt", 'w') as f:
        f.write(str(change.revid) + "\n" + change.content)


def compare_edits(title):
    site = Site('en.wikipedia.org')
    page = site.pages[title]

    # collect metadata information
    metadata = [rev for rev in page.revisions()]
    users = get_users(metadata)
    kind = get_kind(metadata)

    # collect revision contents
    content = []

    for cur in page.revisions(prop='content'):
        if cur.__len__() is 1:
            content.append(prev)
        else:
            content.append(cur)

        prev = cur

    # pre-set first element
    prev = mw.parse(content[0].items()[2]).strip_code().encode('utf-8').split()

    changes = []

    for i in range(1, metadata.__len__()-1):

        # isolate the body text of the revision (cur.items()[2])
        # then, parse the body text with mw (mw.parse())
        # then, use mw to turn the markup text into plain text (.stripcode())
        # then, convert to a utf-8 string using .encode
        text = mw.parse(content[i].items()[2]).strip_code().encode('utf-8')

        cur = text.split()

        change = Change(i, title, metadata[i]['revid'], kind[i], users[i], metadata[i]['comment'], text,
                        added(cur, prev), added(prev, cur))

        changes.append(change)
        write_change(change)
        write_content(change)

        # iterate
        prev = cur

    # out the full list of differences
    return changes


def main():
    title = 'Up (2009 film)'

    changes = compare_edits(title)

    for change in changes:
        print change.removed


main()
