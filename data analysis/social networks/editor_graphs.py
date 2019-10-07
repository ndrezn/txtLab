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
import pycairo
from progress.bar import Bar
import pandas as pd
import sys
import numpy
import random

def get_documents(directory, medium):
	file_list = [f for f in os.listdir(directory) if not f.startswith('.')]
	total_edits = 0
	spam = 0

	files = [(directory+file) for file in file_list]

	files = random.sample(files, 3)

	# multiprocessing (smaller sets)
	pool = Pool()
	documents = pool.map(simple_read_json, files)	# process iterable
	pool.close()

	for document in documents:
		for edit in document:
			edit.medium = medium

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
	# for edge in edges:
	# 	editors[str(edge[0].user)] = len(edge)


	# with open("/Volumes/KINGSTON/txtlab/may-21/editors.json", "w") as outfile:
	# 	json.dump(editors, outfile)

	return edges


def build_graph(edges, g):
	# create a graph using the list of list
	bar = Bar('Finding edges...', max=len(edges))

	edges = numpy.array([numpy.array(edge) for edge in edges])

	# for edge in edges:
	# 	bar.next()
	# 	while (len(edge) > 1):
	# 		cur,edge = edge[-1], edge[:-1]
	# 		for ref in edge:
	# 			try: 
	# 				eid = g.get_eid(cur.title, ref.title, error=False)
	# 			except: 
	# 				continue
	# 			if eid >= 0:
	# 				g.es[eid]['weight'] += 1
	# 			else:
	# 				g.add_edge(cur.title, ref.title, weight=1)
	# bar.finish()

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


def generate_graph(documents, i):
	g = Graph()
	# one node for every novel/film/tv
	g.add_vertices(len(documents))

	meta = pd.read_pickle("/Volumes/NATHAN/out/metadata/improved_meta/complete.pkl")

	titles = []
	mediums = []
	genres = []
	years = []

	bar = Bar('Processing documents...', max=len(documents))

	# iterate through each film/tv/novel
	for document in documents:
		bar.next()
		# add a new node for each title and mark the genre of that title
		if len(document) > 0:
			title = document[0].title
			title.replace(" ", "_")
			titles.append(document[0].title)
			try:
				mediums.append(document[0].medium)
			except:
				mediums.append(None)
			try:
				genre = meta.loc[meta.title == title, 'genre'].tolist()[0]
				if genre is False:
					genres.append(None)
				else:
					genres.append(genre)
			except:
				genres.append(None)
			try:
				years.append(meta.loc[meta.title == title, 'year'].tolist()[0])
			except:
				years.append(None)
	bar.finish()
	g.vs['name'] = titles
	g.vs['medium'] = mediums
	g.vs['genre'] = genres
	g.vs['year'] = years

	# flatten list of edits for each item into one list of all edits
	edits = [item for sublist in documents for item in sublist]
	# sort edits by user
	edits.sort(key=lambda x: x.user)

	
	# ignored_editors = editors_to_ignore(i)

	# for edit in edits:
	# 	if edit.user in ignored_editors:
	# 		edits.remove(edit)

	edges = compile_edges(edits)

	g = build_graph(edges, g)

	print("Graph created.")
	
	return g


# returns a list of editors who have made more than a certain count of edits in the entire space
def editors_to_ignore(i):
	with open("/Volumes/KINGSTON/txtlab/may-21/editors_all.json", encoding = 'utf-8', errors = 'ignore') as json_data:
		d = json.load(json_data)

	users= []
	for key,value in d.items():
		if value > i:
			users.append(key)
	return users


def main():
	for i in range(50):
		mediums = ['films', 'novels', 'tv']
		documents = []
		# directory of jsons to be parsed
		for medium in mediums:
			print("Getting documents for " + medium + ".")
			directory = "/Volumes/NATHAN/out/complete_articles/all/" + medium + "/"
			documents += get_documents(directory, medium)
		g = generate_graph(documents, 28)
		g.write_graphml("/Volumes/NATHAN/out/social networks/random_samples/small/" + str(i) + ".GraphML")
		print("Completed graph " + str(i))


if __name__ == '__main__':
	start = timeit.default_timer()
	main()
	stop = timeit.default_timer()
	print('Time:', stop - start)