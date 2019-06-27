# Generates a visualization of average edits by year of release based on the metadata sheets

library(ggplot2)
library(plotly)
library(plyr)
library(dplyr)

films <- read.csv("/Users/nathandrezner/OneDrive - McGill University/McGill/txt Lab/out/metadata/films.csv", header = TRUE)
novels <- read.csv("/Users/nathandrezner/OneDrive - McGill University/McGill/txt Lab/out/metadata/novels.csv", header = TRUE)
tv <- read.csv("/Users/nathandrezner/OneDrive - McGill University/McGill/txt Lab/out/metadata/tv_shows.csv", header = TRUE)

novels_edits <- data.frame(year = novels[,3], edits = novels[,5])
films_edits <- data.frame(year = films[,7], edits = films[,8])
tv_edits <- data.frame(year = tv[,7], edits = tv[,8])
novels_reversions <- data.frame(year = novels[,3], edits = novels[,9])



# total novel edits
novels_edit_count <- ggplot(novels_edits, aes(x = year, y = edits)) +
  geom_col(show.legend = FALSE)+
  scale_y_discrete(breaks = seq(0, 25000, 3000), limits = 0:25000)+
  labs(title ="Total number of edits for listed novels released in a given year")

novels_edit_count

# total film edits
films_edit_count <- ggplot(films_edits, aes(x = year, y = edits)) +
  geom_col(show.legend = FALSE)+
  scale_y_discrete(breaks = seq(0, 85000, 10000), limits = 0:85000)+
  labs(title ="Total number of edits for listed films released in a given year")

films_edit_count

# AVERAGE NOVELS EDITS
# remove NA values from initial list
novels_edits_no_na <- na.omit(novels_edits)

# convert values to numeric/integer
novels_edits_no_na[] <- lapply(novels_edits_no_na, function(x) {
  if(is.factor(x)) as.numeric(as.character(x)) else x
})
sapply(novels_edits_no_na, class)

# remove NA values again
novels_edits_no_na <- na.omit(novels_edits_no_na)

# create data frame of average edits per year
avg_novels_edits = aggregate(list(edits = novels_edits_no_na$edits), list(year = factor(novels_edits_no_na$year)), mean)

# generate graph from data frame
novels_edit_count <- ggplot(avg_novels_edits, aes(x = year, y = edits)) +
  geom_col(show.legend = FALSE)+
  scale_y_discrete(breaks = seq(0, 25000, 100), limits = 0:1000)+
  scale_x_discrete(breaks = seq(0, 2050, 50))+
  labs(title ="Average number of edits for listed novels released in a given year")

ggplotly(novels_edit_count)

# AVERAGE FILMS EDITS
films_edits_no_na <- na.omit(films_edits)

films_edits_no_na[] <- lapply(films_edits_no_na, function(x) {
  if(is.factor(x)) as.numeric(as.character(x)) else x
})
sapply(films_edits_no_na, class)

films_edits_no_na <- na.omit(films_edits_no_na)

avg_film_edits = aggregate(list(edits = films_edits_no_na$edits), list(year = factor(films_edits_no_na$year)), mean)

films_edit_count <- ggplot(avg_film_edits, aes(fill = year, x = year, y = edits)) +
  geom_col(show.legend = FALSE)+
  scale_y_discrete(breaks = seq(0, 25000, 100), limits = 0:1000)+
  scale_x_discrete(breaks = seq(0, 2050, 25))+
  theme_dark()+
  labs(title ="Average number of edits for listed films released in a given year")

ggplotly(films_edit_count)

# AVERAGE NOVELS REVERSIONS
novels_reversions_no_na <- na.omit(novels_reversions)

novels_reversions_no_na[] <- lapply(novels_reversions_no_na, function(x) {
  if(is.factor(x)) as.numeric(as.character(x)) else x
})
sapply(novels_reversions_no_na, class)

novels_reversions_no_na <- na.omit(novels_reversions_no_na)

avg_novels_reversions = aggregate(list(edits = novels_reversions_no_na$edits), list(year = factor(novels_reversions_no_na$year)), mean)

novels_reversions_count <- ggplot(avg_novels_reversions, aes(x = year, y = edits)) +
  geom_col(show.legend = FALSE)+
  scale_y_discrete(breaks = seq(0, 25000, 100), limits = 0:1000)+
  scale_x_discrete(breaks = seq(0, 2050, 50))+
  labs(title ="Average number of reversions for listed novels released in a given year")

ggplotly(novels_reversions_count)
