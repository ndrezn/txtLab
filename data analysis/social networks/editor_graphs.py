## generates a graph from the raw json files of edit histories for the pages
# In the generated graph: Each node represents an article, and each edge represents whether
# the connected nodes share an editor. The weight of the edges is the number of users who edited
# both articles.

## for instance, if three users edited both "The Dark Knight" and "Game of Thrones", then there is an
## edge between those two nodes with a weight of three.

from igraph import *
from wiki_page import *
from multiprocessing import Pool
import pycairo


def get_documents(directory, medium):
	file_list = [f for f in os.listdir(directory) if not f.startswith('.')]
	total_edits = 0
	spam = 0

	files = [(directory+file) for file in file_list]

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
	for cur in edits:
		if cur.user == ref.user:
			if cur.title not in [x.title for x in edge]:
				edge.append(cur)
		else:
			edges.append(edge)
			ref = cur
			edge = [ref]

	editors = {}
	for edge in edges:
		editors[str(edge[0].user)] = len(edge)


	with open("/Volumes/KINGSTON/txtlab/may-21/editors.json", "w") as outfile:
		json.dump(editors, outfile)

	return edges


def build_graph(edges, g):
	# create a graph using the list of lists
	for edge in edges:
		while (len(edge) > 1):
			cur = edge.pop()
			for ref in edge:
				try: 
					eid = g.get_eid(cur.title, ref.title, error=False)
				except: 
					continue
				if eid >= 0:
					g.es[eid]['weight'] += 1
				else:
					g.add_edge(cur.title, ref.title, weight=1)
	return g


def generate_graph(documents, i):
	g = Graph()
	# one node for every novel/film/tv
	g.add_vertices(len(documents))

	titles = []
	mediums = []
	# iterate through each film/tv/novel
	for document in documents:
		# add a new node for each title and mark the genre of that title
		if len(document) > 0:
			titles.append(document[0].title)
			mediums.append(document[0].medium)

	g.vs['name'] = titles
	g.vs['medium'] = mediums

	# flatten list of edits for each item into one list of all edits
	edits = [item for sublist in documents for item in sublist]
	# sort edits by user
	edits.sort(key=lambda x: x.user)

	
	ignored_editors = editors_to_ignore(i)

	# for edit in edits:
	# 	if edit.user in ignored_editors:
	# 		edits.remove(edit)

	print("Graph metadata complete.")

	edges = compile_edges(edits)

	print("Edges compiled.")

	g = build_graph(edges, g)

	print("Graph created.")
	
	return g


def plot_graph(g):
	g.write_graphml("/Volumes/KINGSTON/txtlab/out/social networks/sans_major_editors.GraphML")


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
	mediums = ['novels', 'films', 'tv']
	documents = []
	# directory of jsons to be parsed
	print("Starting...")
	for medium in mediums:
		directory = "/Volumes/KINGSTON/txtlab/jsons/" + medium + "/"
		documents += get_documents(directory, medium)
	print("Done collecting objects.")

	g = generate_graph(documents, 28)

	plot_graph(g)

	print("Done.")


if __name__ == '__main__':
	start = timeit.default_timer()
	main()
	stop = timeit.default_timer()
	print('Time:', stop - start)