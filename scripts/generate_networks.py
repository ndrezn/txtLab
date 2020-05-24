'''
Network builder
In the generated graph: Each node represents an article, and each edge represents whether
the connected nodes share an editor. The weight of the edges is the number of users who edited
both articles.

for instance, if three total users edited both "The Dark Knight" and "Game of Thrones", then there is an
edge between those two nodes with a weight of three.
'''

import networkx as nx
from progress.bar import Bar
import pandas as pd
import sys
import numpy
import random
import re
from progress.bar import IncrementalBar
import time



def get_documents(
    domain, size  # domain can be 'sciences', 'sports', 'politics', or 'culture'
):
    metadata = "./results/data-sets/category-sampling/metadata_sheets/metadata.csv"
    data = "./results/data-sets/category-sampling/"

    meta_types = {}
    types = []

    df = pd.read_csv(metadata)

    # pick two random submediums from which to draw documents if we're picking from all
    # (e.g. ('democrat', 'biology') or ('republican', 'democrat'))
    if domain is not 'all':
        df = df.loc[df['Domain']==domain]
    selected_categories = random.sample(df["Category"].unique().tolist(), 2)
    
    # clear out rows of the dataframe which don't match the selected types
    container = pd.DataFrame()
    for c in selected_categories:
        cur = df.loc[df['Category'] == c]
        cur = cur.sample(n=int(size/2))
        container = pd.concat([container, cur])

    return container


def get_users(name, domain):
    fpath = "./results/data-sets/category-sampling/" + domain + "/" + name + ".csv"

    try:
        df = pd.read_csv(fpath)
    except: # In case the data isn't there
        return None

    return list(df["User"])


def intersection(lst1, lst2): # Get the intersection of two lists, O(n) time
    # Use of hybrid method
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3


def build_graph(df):
    df["Users"] = df.apply(
        lambda row: get_users(row["Pages"], row["Domain"]), axis=1
    )  # get the user lists for each page

    df = df.dropna(subset=["Users"])

    g = nx.Graph()
    # one node for every novel/film/tv
    g.add_nodes_from(list(df["Pages"]))


    attrs = {}
    for i, row in df.iterrows():
        attrs[row["Pages"]] =  {"domain": row["Domain"], "category": row["Category"]}

    nx.set_node_attributes(g, attrs)

    for i1, row1 in df.iterrows():  # iterate through all nodes and user lists
        node1 = row1['Pages']
        users1 = row1['Users']
        for i2, row2 in df.iterrows():  # iterate through all other nodes and user lists
            node2 = row2['Pages']
            if node1==node2:
                continue
            users2 = row2['Users']
            if not g.has_edge(
                node1, node2
            ):  # if there is not an edge between the two nodes
                common_users = intersection(users1, users2)  # get the common users
                g.add_edge(
                    node1, node2, weight=len(common_users)
                )  # add an edge to the network with a weight of the common users

    return g


def main():
    mediums = ["all",'culture', 'politics','sciences','sports']

    count = 1000
    size = 300
    bar = IncrementalBar('Building networks... ', max=count)
    for medium in mediums:
        for i in range(0, count):
            documents = []
            # directory of jsons to be parsed
            documents = get_documents(medium, size)
            g = build_graph(documents)
            path = ("./results/data-sets/social-networks/"+medium+"/"+str(i)+".GraphML")
            nx.write_graphml(g, path)
            bar.next()

    bar.finish()

main()
