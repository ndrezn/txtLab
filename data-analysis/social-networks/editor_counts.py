## counts the total number of edits in the space of collected articles by each editor
## and outputs a json file containing all the editors and the number of edits each of them made.

from wiki_page import *
import json
import timeit
from multiprocessing import Pool


def get_documents(directory, genre):
    file_list = [f for f in os.listdir(directory) if not f.startswith(".")]
    total_edits = 0
    spam = 0

    files = [(directory + file) for file in file_list]

    pool = Pool()
    documents = pool.map(simple_read_json, files)  # process iterable
    pool.close()

    for document in documents:
        for edit in document:
            edit.genre = genre

    return documents


def main():
    genres = ["novels", "films", "tv"]
    documents = []
    # directory of jsons to be parsed
    print("Starting...")
    for genre in genres:
        directory = "/Volumes/KINGSTON/txtlab/jsons/" + genre + "/"
        documents += get_documents(directory, genre)
    print("Done collecting objects.")

    editor_counts = {}

    edits = [item for sublist in documents for item in sublist]

    for edit in edits:
        if edit.user in editor_counts:
            editor_counts[edit.user] += 1
        else:
            editor_counts[edit.user] = 1

    with open("/Volumes/KINGSTON/txtlab/may-21/editors_all.json", "w") as outfile:
        json.dump(editor_counts, outfile)


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print("Time:", stop - start)
