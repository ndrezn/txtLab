import pandas as pd
from wiki_page import *
from datetime import datetime, date, time
from progress.bar import Bar
from statistics import mean

# imports for counting added words
from collections import Counter
import re
from multiprocessing import Pool

# number of human and bot reversions to the page
def count_reversions(document):
    reversions = 0
    human_reversions = 0

    for version in document:
        comment = version.comment.lower()
        user = version.user.lower()

        if "revert" in comment or "undid" in comment:
            reversions += 1
            if "bot" not in user and "bot" not in comment:
                human_reversions += 1

    return reversions, human_reversions


# number of edits to the page
def count_edits(document):
    return len(document)


# get the length of the most recent article version
def article_length(document):
    text = document.pop()
    return len(text.content.split(" "))


# dict of users and number of edits they contributed to the pate
def count_users_and_ratings(document):
    users = {}
    ratings = {}
    times = []
    for version in document:
        user = version.user.lower()
        rating = version.rating.lower()

        if user not in users:
            users[user] = 1
        else:
            users[user] += 1
        if rating not in ratings:
            ratings[rating] = 1
            times.append(datetime.strptime(version.time, "%Y-%m-%d %H:%M:%S"))
        else:
            ratings[rating] += 1

    counted_times = []
    if len(times) > 1:
        fst = times.pop(0)

        for cur in times:
            diff = abs((fst - cur).total_seconds())
            diff = diff / 3600
            counted_times.append(diff)
            fst = cur
        avg_time = mean(counted_times)
    else:
        avg_time = None

    return users, (ratings, avg_time)


# average time between each edit
def average_time(document):
    datetimes = [
        datetime.strptime(version.time, "%Y-%m-%d %H:%M:%S") for version in document
    ]
    if len(datetimes) < 2:
        return None, None
    fst = datetimes.pop(0)

    total_time = 0
    total_short_edits = 0
    num_short_edits = 0

    for cur in datetimes:
        diff = abs((fst - cur).total_seconds())
        diff = diff / 3600

        if diff < 720:
            total_short_edits += diff
            num_short_edits += 1

        total_time += diff
        fst = cur

    avg = total_time / len(datetimes)
    if num_short_edits < 2:
        return avg, None
    else:
        avg_short = total_short_edits / num_short_edits
    return avg, avg_short


# time / date the first edit was made
def first_time(document):
    datetimes = [
        datetime.strptime(version.time, "%Y-%m-%d %H:%M:%S") for version in document
    ]
    return datetimes.pop(0)


# count the number of minor edits
def total_minor(document):
    minor = 0
    for version in document:
        minor += int(version.kind)
    return minor


# Get the json file and convert it to an object
def get_document(url, genre):
    if "/" in url:
        url = url.split("/")[2]
    file = "/Volumes/NATHAN/out/complete_articles/all/" + genre + "/" + url + ".json"
    try:
        return read_json(file)
    except:
        return None


# FOR COUNTING ADDED WORDS
# create vector of word counts for a single document
def create_collection(text):
    c = Counter(
        # set to lower case
        word.lower()
        # remove punctuation
        for word in re.findall(r"\b[^\W\d_]+\b", text)
    )
    return c


# create an array of differential vectors representing
# changes between each page
def successors(vectors):
    prev = Counter()

    changes = []
    for cur in vectors:
        # copy current document
        temp = Counter(cur)
        # subtract the previous document from the current document
        temp.subtract(prev)
        # add the differential vector to an array
        changes.append(temp)
        # iterate the previous document
        prev = cur
    return changes


# add together all the additions (positive vector counts) into one counter
# add together all removals (negative vector counts) into another counter
def compile(changes):
    added, removed = Counter(), Counter()
    for vec in changes:
        # for each (word, count) tuple in the vector
        for k in vec.items():
            # if the count is positive (added word) increase count for that
            # word by the count in the vector
            if k[1] > 0:
                added[k[0]] += k[1]
            elif k[1] < 0:
                removed[k[0]] -= k[1]

    return added, removed


# check the type token ration and confirm it is valid
def check_type_token(unique_words, total_words):
    if unique_words > 0:
        if unique_words / total_words > 0.1:
            return True
    return False


def get_added_words(document):
    # document represents the complete set of revisions
    # for each revision in the document of revisions
    texts = [item.content for item in document]

    # multiprocess the collections
    pool = Pool(os.cpu_count())  # create a pool
    collections = pool.map(create_collection, texts)  # process iterable
    pool.close()

    vecs = []
    for parsed in collections:
        # get the number of unique words and total number of words
        unique_words = len(parsed)
        total_words = sum(parsed.values())
        # if there is content in the text
        if check_type_token(unique_words, total_words):
            # check that type_token ratio is above 10%
            # create a counter for the document
            vecs.append(parsed)

    # create list of vectors between each document
    changes = successors(vecs)
    # compile vectors between each document
    added_words, removed_words = compile(changes)

    return added_words, removed_words


def main():
    genres = ["politics"]
    for genre in genres:
        meta = pd.read_csv("/Volumes/NATHAN/" + genre + ".csv")

        meta["Document"] = meta.apply(
            lambda row: get_document(row["URL"], genre), axis=1
        )
        meta.dropna(subset=["Document"])
        print("Documents collected.")
        meta["Reversions"], meta["Human reverts"] = zip(
            *meta.apply(lambda row: count_reversions(row["Document"]), axis=1)
        )
        meta["Edits"] = meta.apply(lambda row: count_edits((row["Document"])), axis=1)
        (
            meta["Average time between edits"],
            meta["Average time between edits (for edits less than one month apart)"],
        ) = zip(*meta.apply(lambda row: average_time((row["Document"])), axis=1))
        meta["Minor edits"] = meta.apply(
            lambda row: total_minor((row["Document"])), axis=1
        )
        meta["Time of first edit"] = meta.apply(
            lambda row: first_time((row["Document"])), axis=1
        )
        meta["Length of current version"] = meta.apply(
            lambda row: article_length((row["Document"])), axis=1
        )

        users, ratingstimes = zip(
            *meta.apply(lambda row: count_users_and_ratings((row["Document"])), axis=1)
        )
        meta["Ratings"], meta["Time between rating changes"] = zip(*ratingstimes)
        meta["Users"] = users
        meta["Added words"], meta["Removed words"] = zip(
            *meta.apply(lambda row: get_added_words((row["Document"])), axis=1)
        )

        del meta["Document"]
        print(meta)
        meta.to_csv("/Volumes/NATHAN/" + genre + "_meta.csv")


main()
