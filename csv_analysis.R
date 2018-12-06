library(DataExplorer)


f = read.csv("csv_outputs/films.csv")

plot_str(f)

plot_histogram(f)


plot_density(f)


summary(f)

str(f)

