library(igraph)

g <- read_graph(file="/Volumes/KINGSTON/txtlab/out/social networks/graphs/laymen only.GraphML", format='graphml')

c <- fastgreedy.community(g)

plot_dendrogram(c)
