from igraph import *
from wiki_page import *
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
        while len(edge) > 1:
            cur = edge.pop()
            for ref in edge:
                eid = g.get_eid(cur.title, ref.title, error=False)
                if eid >= 0:
                    g.es[eid]["weight"] += 1
                else:
                    g.add_edge(cur.title, ref.title, weight=1)
    return g


def generate_graph(documents, i):
    g = Graph()
    # one node for every novel/film/tv
    g.add_vertices(len(documents))

    titles = []
    genres = []
    # iterate through each film/tv/novel
    for document in documents:
        # add a new node for each title and mark the genre of that title
        if len(document) > 0:
            titles.append(document[0].title)
            genres.append(document[0].genre)

    g.vs["name"] = titles
    g.vs["genre"] = genres

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
    g.write_graphml("/Volumes/KINGSTON/txtlab/out/social networks/all_novels.GraphML")


# returns a list of editors who have made more than a certain count of edits in the entire space
def editors_to_ignore(i):
    with open(
        "/Volumes/KINGSTON/txtlab/may-21/editors_all.json",
        encoding="utf-8",
        errors="ignore",
    ) as json_data:
        d = json.load(json_data)

    users = []
    for key, value in d.items():
        if value > i:
            users.append(key)
    return users


def main():
    years = range(1997, 1998)
    documents = []
    # directory of jsons to be parsed
    print("Starting...")
    for year in years:
        if year % 10 is 0:
            print(year)
        directory = "/Volumes/KINGSTON/txtlab/jsons/full_novels/" + str(year) + "/"
        try:
            documents += get_documents(directory, year)
        except:
            continue
    print("Done collecting objects.")

    g = generate_graph(documents, 28)

    plot_graph(g)

    print("Done.")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print("Time:", stop - start)
