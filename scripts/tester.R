#install.packages("rvest")

library(rvest)

# Store web url
films <- read_html("https://en.wikipedia.org/wiki/List_of_American_films_of_1960")

#Scrape the table for the list
titles <- films %>% #pipe variable into next line
  html_nodes(".wikitable td:nth-child(1)") %>% #read data from specific html node
  html_text() #convert to text

directors <- films %>%
  html_nodes(".wikitable td:nth-child(2)") %>%
  html_text()

cast <- films %>%
  html_nodes("td:nth-child(3)") %>%
  html_text()

genres <- films %>%
  html_nodes("td:nth-child(4)") %>%
  html_text()

#convert into a data set
table1910 <- data.frame(titles, directors, cast, genres)
