library(DTK)

my_data <- read.csv("/Volumes/NATHAN/out/metadata/improved_meta/genres.csv")

my_data

attach(my_data)

results = DTK.test(edits, genre,0.05)
results
DTK.plot(results)
