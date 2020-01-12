## random small graphs
## generates a graph from the raw json files of edit histories for the pages
# In the generated graph: Each node represents an article, and each edge represents whether
# the connected nodes share an editor. The weight of the edges is the number of users who edited
# both articles.

## for instance, if three total users edited both "The Dark Knight" and "Game of Thrones", then there is an
## edge between those two nodes with a weight of three.

from igraph import *
from wiki_page import *
from multiprocessing import Pool
from progress.bar import Bar
import pandas as pd
import sys
import numpy
import random
import re

def get_documents(m, size):
	directory = '/Volumes/NATHAN/metadata/simple_metadata/'
	json_dir = '/Users/dh_lab_01/Desktop/out/'

	meta_types = {}
	types = []

	if m is 'all':
		mediums = ['culture', 'politics', 'science', 'sports']
	else:
		mediums = [m]
	
	df = pd.DataFrame()
	for medium in mediums:
		cur_df = pd.read_csv(directory+medium+'.csv')
		cur_df['MEDIUM'] = medium
		df = df.concat(df, cur_df)
	
	# pick two random submediums from which to draw documents
	# (e.g. ('democrat', 'biology') or ('republican', 'democrat'))
	selected_submediums = random.sample(df['Type'].unique().tolist(), 2)

	# clear out rows of the dataframe which don't match the selected types
	df = df.loc[df['Type'].isin(selected_submediums)]
	
	documents = []	
	# iterate through the mediums which ended up in the dataframe (could be either 1 or 2)
	for medium in df['MEDIUM'].unique().tolist():
		# make the dataframe so it's only the items from the mediums we want (this way the files can be selected)
		cur = df.loc[df['MEDIUM']==medium]
		# create a list of possible files based on the dataframe
		df_files = [re.sub('/wiki/', '', f)+'.json' for f in cur['URL'].tolist()]
				
		# get a list of actual files from the json directory
		directory_files = [f for f in os.listdir(json_dir+medium) if not f.startswith('.')]
		
		# generate a list of file paths where the file is in both the directory and in the dataframe
		actual_files = [json_dir + medium + '/' + f for f in directory if f in df_files]
		
		# make sure there are enough files for the sample size
		if len(file_list) < size: 
			# if not, try again
			get_documents(medium, size)
		
		# randomly pick out the files we want
		file_list = random.sample(file_list, size)
		
		# read the files in as 
		# multiprocessing (smaller sets)
		pool = Pool()
		docs = pool.map(simple_read_json, file_list)	# process iterable
		pool.close()
		for document in docs:
			for edit in document:
				edit.medium = medium

		documents += docs
	
	return documents


def compile_edges(edits):
	# reference user
	ref = edits.pop()
	# list of movies a user has touched, starting with the reference
	edge = [ref]
	edges = []
	# create a list of lists representing the set of movies each user has touched
	bar = Bar('Building edge data...', max=len(edits))
	for cur in edits:
		bar.next()
		if cur.user == ref.user:
			if cur.title not in [x.title for x in edge]:
				edge.append(cur)
		else:
			edges.append(edge)
			ref = cur
			edge = [ref]

	editors = {}
	bar.finish()

	return edges


def build_graph(edges, g):
	# create a graph using the list of list
	bar = Bar('Finding edges...', max=len(edges))

	edges = numpy.array([numpy.array(edge) for edge in edges])

	edgelist = []
	for edge in edges:
		bar.next()
		while (len(edge) > 1):
			cur,edge = edge[-1], edge[:-1]
			for ref in edge:
				edgelist.append((cur.title,ref.title))
	bar.finish()

	bar = Bar('Generating graph...', max=len(edgelist))

	for (node1,node2) in edgelist:	
		bar.next()
		eid = g.get_eid(node1,node2, error=False)
		if eid >= 0:
			g.es[eid]['weight'] += 1
		else:
			g.add_edge(node1, node2, weight=1)

	bar.finish()

	return g


def generate_graph(documents):
	g = Graph()
	# one node for every novel/film/tv
	g.add_vertices(len(documents))


	titles = []
	genres = []
	edits = []
	# iterate through each film/tv/novel
	for m, document in documents.items():
		meta = pd.read_csv("/Volumes/NATHAN/metadata/simple_metadata/"+m+".csv")
		bar = Bar('Processing documents...', max=len(document))

		for item in document:
			bar.next()
			# add a new node for each title and mark the genre of that title
			if len(item) > 0:
				if m != "politics":
					title = "/wiki/"+item[0].title
				else:
					title = item[0].title
				titles.append(item[0].title)
				genre = meta.loc[meta.URL == title, 'Type'].tolist()[0]
				if genre is False:
					genres.append(None)
				else:
					genres.append(genre)

		bar.finish()

		# flatten list of edits for each item into one list of all edits
		edits += [item for sublist in document for item in sublist]
	print(titles)
	g.vs['name'] = titles
	g.vs['genre'] = genres
	print(g.vs['name'])

	# sort edits by user
	edits.sort(key=lambda x: x.user)

	edges = compile_edges(edits)

	g = build_graph(edges, g)

	print("Graph created.")
	
	return g


def main():
	medium = 'all'
	
	for i in range(0, 1000):
		documents = []
		# directory of jsons to be parsed
		print("Getting documents for " + medium + ".")

		documents = None
		while documents is None:
			documents = get_documents(medium, 20)
		g = generate_graph(documents)
		g.write_graphml("/Volumes/NATHAN/social_networks/"+medium+"/" + str(i) + ".GraphML")
		print("Completed graph " + str(i))


start = timeit.default_timer()
main()
stop = timeit.default_timer()
print('Time:', stop - start)