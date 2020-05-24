'''
Get the 
'''

import igraph
import networkx as nx
from statistics import stdev, mean
import os
import operator
import pandas as pd
from progress.bar import IncrementalBar



def get_louvain(g):
    '''
    LOUVAIN ALGORITHM
    This is a bottom-up algorithm: initially every vertex belongs to a separate community,
    and vertices are moved between communities iteratively in a way that maximizes the
    vertices' local contribution to the overall modularity score. When a consensus is
    reached (i.e. no single move would increase the modularity score), every community in
    the original graph is shrank to a single vertex (while keeping the total weight of the
    adjacent edges) and the process continues on the next level. The algorithm stops when it
    is not possible to increase the modularity any more after shrinking the communities to vertices.
    '''
    louvain = g.community_multilevel(weights=[weight for weight in g.es["weight"]])
    return louvain


def purity(attribute, louvain, graph):
    '''
    Get the average purity score for the two largest networks in a graph given an attribute to check the purity of
    Usually this attribute will be 'category'
    '''
    unique_types = list(set([v[attribute] for v in graph.vs]))
    louvain = sorted(list(louvain), key=len)[-2:]

    purity = []
    for group in louvain:
        categories = []
        for node in group:
            cur = unique_types.index(graph.vs[attribute][node])
            categories.append(cur)
        count_cat0 = categories.count(0)
        count_cat1 = categories.count(1)

        purity.append(max(count_cat1, count_cat0)/len(group))

    return mean(purity)


def get_assortativity(file):
    g = nx.read_graphml(file)

    a = nx.attribute_assortativity_coefficient(g,'category')
    print(a)
    return a


def get_purity(file):
    g = igraph.load(file)
    louv = get_louvain(g)
    p = purity('category', louv, g)
    return p


def main():
    kinds = ['all', 'culture', 'sports', 'politics', 'sciences']
    
    df = []
    for kind in kinds:
        directory = "results/data-sets/social-networks/" + kind + "/"

        files = [directory+f for f in os.listdir(directory) if not f.startswith(".")]
        bar = IncrementalBar(kind+'... ', max=len(files))

        for file in files:
            bar.next()
            cur = {}
            p = get_purity(file)
            a = get_assortativity(file)
            cur['assortativity'] = a
            cur['purity'] = p
            cur['kind'] = kind
            df.append(cur)

        bar.finish()

    df = pd.DataFrame(df)
    print(df)
    df.to_csv('results/data-sets/social-networks/metadata.csv')


def test():
    G=nx.Graph()
    G.add_nodes_from([0,1],color='red')
    G.add_nodes_from([2,3],color='blue')
    G.add_edges_from([(0,1),(2,3), [2,1], [2,0]])
    print(nx.attribute_assortativity_coefficient(G,'color'))



main()
