## Generates a metadata sheet from Wikipedia's list of American Television Programs

from bs4 import BeautifulSoup
import requests
import csv
from codecs import open
import pandas


def get_meta():
    url = "https://en.wikipedia.org/wiki/List_of_American_television_programs"
    # make soup
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")

    urls = []
    metas = []
    titles = []

    items = filter(None, soup.findAll("li"))

    for item in items:
        try:
            title = item.i.a.find(text=True, recursive=False).strip()
            url = item.i.a["href"]
            meta = item.find(text=True, recursive=False).strip()
        except:
            continue

        titles.append(title)
        urls.append(url)
        metas.append(meta)

    starts = []
    ends = []
    genres = []
    for meta in metas:
        split = meta.split(")")
        years = split[0][1:].split("–")

        try:
            start = int(years[0])
        except:
            start = 0
        starts.append(start)

        try:
            ends.append(years[1])
        except:
            ends.append("NA")

        try:
            genres.append(split[1].strip()[2:])
        except:
            genres.append("NA")

    meta = pandas.DataFrame()
    meta["title"] = titles
    meta["url"] = urls
    meta["genre"] = genres
    meta["year"] = starts
    meta["end"] = ends

    print(meta.loc[meta["year"] == 0])  # something like this)

    return meta


def main():
    meta = get_meta()

    out = "/Volumes/KINGSTON/txtlab/out/metadata/tv2.csv"

    meta.to_csv(out)


main()
