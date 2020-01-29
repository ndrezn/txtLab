# graphs based on the full metadata sheet

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from statistics import stdev, mean


def count(item):
    if item > 1000:
        return None
    return item


# columns = ',title,medium,year,genre,edits,users,ratings,reverts,human_reverts,rating_times,avg_time,avg_time_short,minor'


def graph_release():
    meta = pd.read_pickle("/Volumes/NATHAN/out/metadata/improved_meta/complete2.pkl")
    meta = meta[(meta["year"] > 1800)]

    fig, ax = plt.subplots()
    ax = meta.boxplot("year", ax=ax, by="medium")

    fig.suptitle("Distribution of articles by year of release")
    ax.set_ylabel("Year of release")

    plt.show()


def graph_edits():
    meta = pd.read_pickle("/Volumes/NATHAN/out/metadata/improved_meta/complete2.pkl")
    dfs = {}
    genres = {}
    mediums = ["films", "novels", "tv"]
    meta = meta[pd.notnull(meta["edits"])]
    for medium in mediums:
        dfs[medium] = meta.loc[meta["year"] > 0]
        dfs[medium] = dfs[medium].loc[meta["medium"] == medium]
        genres[medium] = dfs[medium]["genre"].unique()
        dfs[medium] = dfs[medium].reset_index()

    cur = pd.DataFrame({})
    yearly_averages = pd.DataFrame()

    for medium, df in dfs.items():
        g = df.groupby(["year"], as_index=False)
        cur = g.agg({"edits": np.mean})
        cur["medium"] = medium

        yearly_averages = pd.concat([yearly_averages, cur], ignore_index=True)

    yearly_averages = yearly_averages[(yearly_averages["medium"] == "novels")]

    yearly_averages = yearly_averages.sort_values(by="edits")
    print(yearly_averages)

    exit()

    fig, ax = plt.subplots()
    for key, grp in yearly_averages.groupby(["medium"]):
        ax = grp.plot(
            ax=ax,
            kind="line",
            x="year",
            y="edits",
            label=key,
            title="Average edits for media released in a given year",
        )
    plt.legend(loc="best")
    plt.show()


def graph_time():
    meta = pd.read_pickle("/Volumes/NATHAN/out/metadata/improved_meta/complete2.pkl")
    fig, ax = plt.subplots()
    ax = meta.boxplot("edits", ax=ax, by="medium")
    fig.suptitle("Number edits for edits across all mediums")
    ax.set_ylabel("Edits")

    plt.show()


def graph_genre():
    meta = pd.read_pickle("/Volumes/NATHAN/out/metadata/improved_meta/complete2.pkl")
    meta["edits"] = meta["edits"].apply(count)
    meta = meta[pd.notnull(meta["edits"])]

    meta = meta[(meta["medium"] == "films")]
    drama = meta[(meta["genre"] == "drama")]
    comedy = meta[(meta["genre"] == "comedy")]
    horror = meta[(meta["genre"] == "horror")]
    western = meta[(meta["genre"] == "western")]

    meta = pd.concat([drama, comedy, horror, western])

    # meta.to_csv("/Volumes/NATHAN/out/metadata/improved_meta/genres.csv")

    fig, ax = plt.subplots()
    ax = meta.boxplot("rating_times", ax=ax, by="genre")
    fig.suptitle("Time for articles to recieve a new quality rating")
    ax.set_ylabel("Average time (hours)")
    plt.show()


def graph_rating_times():
    meta = pd.read_pickle("/Volumes/NATHAN/out/metadata/improved_meta/complete2.pkl")
    fig, ax = plt.subplots()
    ax = meta.boxplot("rating_times", ax=ax, by="medium")
    fig.suptitle("Time for articles to recieve a new quality rating")
    ax.set_ylabel("Average time (hours)")

    plt.show()


def items_from_year(year):
    meta = pd.read_pickle("/Volumes/NATHAN/out/metadata/improved_meta/complete2.pkl")
    meta = meta[(meta["year"] == year)]
    meta = meta[(meta["medium"] == "films")]
    meta = meta.sort_values(by="edits")

    print(meta)


def average_edits():
    meta = pd.read_pickle("/Volumes/NATHAN/out/metadata/improved_meta/complete2.pkl")
    # dfs = {}
    # mediums = ['films', 'novels', 'tv']
    # meta = meta[pd.notnull(meta['edits'])]
    # for medium in mediums:
    #     dfs[medium] = meta.loc[meta['year'] > 0]
    #     dfs[medium] = dfs[medium].loc[meta['medium']==medium]
    #     dfs[medium] = dfs[medium].reset_index()

    # for key,df in dfs.items():
    #     print(key, ": ", mean(df['edits']))

    meta = meta[(meta["medium"] == "films")]
    drama = meta[(meta["genre"] == "drama")]
    comedy = meta[(meta["genre"] == "comedy")]
    horror = meta[(meta["genre"] == "horror")]
    western = meta[(meta["genre"] == "western")]

    print(mean(drama["edits"]))
    print(mean(comedy["edits"]))
    print(mean(horror["edits"]))
    print(mean(western["edits"]))


graph_time()
