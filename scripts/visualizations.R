library(ggplot2)
library(plotly)
library(plyr)
library(dplyr)

films <- read.csv("/Users/nathandrezner/OneDrive - McGill University/McGill/txt Lab/out/metadata/films.csv", header = TRUE)
novels <- read.csv("/Users/nathandrezner/OneDrive - McGill University/McGill/txt Lab/out/metadata/novels.csv", header = TRUE)

novels_edits <- data.frame(year = novels[,3], edits = novels[,5])
films_edits <- data.frame(year = films[,7], edits = films[,8])

#total novel edits
novels_edit_count <- ggplot(novels_edits, aes(x = year, y = edits)) +
  geom_col(show.legend = FALSE)+
  scale_y_discrete(breaks = seq(0, 25000, 3000), limits = 0:25000)+
  labs(title ="Total number of edits for listed novels released in a given year")

novels_edit_count

#total film edits
films_edit_count <- ggplot(films_edits, aes(x = year, y = edits)) +
  geom_col(show.legend = FALSE)+
  scale_y_discrete(breaks = seq(0, 85000, 10000), limits = 0:85000)+
  labs(title ="Total number of edits for listed films released in a given year")

films_edit_count

#average novels edits
novels_edit_count_per <- ggplot(novels_edits, aes(x=factor(year), y=edits)) +
  stat_summary(fun.y="mean", geom="bar") +
  scale_y_discrete(breaks = seq(0, 1000, 200), limits = 0:1000)+
  labs(title ="Average edits per page for listed novels released in a given year")

inter <- ggplotly(novels_edit_count_per)

inter

#average films edits
films_edit_count_per <- ggplot(films_edits, aes(x = year, y = edits)) +
  stat_summary(fun.y="mean", geom="bar") +
  scale_y_discrete(breaks = seq(0, 1000, 200), limits = 0:1100)+
  labs(title ="Average edits per page for listed films released in a given year")

ggplotly(films_edit_count_per)
