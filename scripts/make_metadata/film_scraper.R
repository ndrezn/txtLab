library(rvest)
library(purrr)

#initialize arrays so that the pages are organized for URL scraping
starts_five <- c(31, 36, 52)
starts_six <- c(22, 24, 30:33, 35, 41, 45:46, 48, 55, 57, 59, 84, 88)
starts_seven <- c(12, 15, 17, 26, 28, 29, 34, 38:40, 42, 
                  44, 47, 56, 58, 60, 63:65, 67, 69, 75, 76:77, 94, 99)
starts_nine <- c(27, 43, 62, 66, 68, 70, 74, 80, 90, 93, 98)
starts_ten <- c(37, 81, 86:87)
starts_eleven<- c(53)
starts_thirteen <- c(50:51)

#these are the pages that only have one table and require a different node to be read
different_node <-c(0:12, 14, 23, 83, 101:113)

map_df(1:113, function(i) {
  print(i)
  writeLines("\n")
  
  #Variable name for url
  url <- paste("https://en.wikipedia.org/wiki/List_of_American_films_of_", i+1900, sep = "")
  
  #Read url
  pg <- read_html(url)
  
  #Scrape titles
  title <- html_text(html_nodes(pg, ".wikitable td:nth-child(1)"))

  #Scrape directors
  director <- html_text(html_nodes(pg, ".wikitable td:nth-child(2)"))
  
  #Scrape cast
  cast <- html_text(html_nodes(pg, ".wikitable td:nth-child(3)"))
    
  #Scrape genres
  genre <- html_text(html_nodes(pg, ".wikitable td:nth-child(4)"))
  
  #Scrape notes
  notes <- html_text(html_nodes(pg, ".wikitable td:nth-child(5)"))
  
  #here we go: time to scrap the urls. This takes wayyyy too much effort but whatever
  #initialize the array of urls
  specific_url <- character(length = (length(cast)))
  #counts the current element we're at, in a box. 
  #Indexing starts at 2 and increases by 1
  k <- 2
  #iterates through the length of the list to make sure you don't go too far
  j <- 1
  
  #the following if statements initialize the box number
  #if box starts at 5
  if(i %in% starts_five){
    cur_box <- 5
  }
  
  #if box starts at 6
  else if(i %in% starts_six){
    cur_box <- 6
  }
  
  #if box starts at 7
  else if(i %in% starts_seven){
    cur_box <- 7
  }
  
  #if box starts at 9
  else if(i %in% starts_nine){
    cur_box <- 9
  }
  
  #if box starts at 10
  else if(i %in% starts_ten){
    cur_box <- 10
  }
  
  else if(i %in% starts_eleven){
    cur_box <- 11
  }
  
  else if(i %in% starts_thirteen){
    cur_box <- 13
  }
  
  else{
    cur_box <- 8
  }
  
  #progress bar :)
  pb  <- txtProgressBar(1, length(cast), style=3)
  writeLines("Scraping URLs\n")
  
  #scrape URLs
  while(j <= length(cast)){
    #progress bar
    setTxtProgressBar(pb, j)
    
    #set node to be read
    if(i %in% different_node){
      node <- paste("tr:nth-child(", k, ") i a", sep="")
    }
    
    #set node to be read
    else {
      node <- paste(".wikitable:nth-child(", cur_box, ") tr:nth-child(", k, ") i a", sep="")
    }
    
    #extract url into table
    specific_url[j] <- pg %>%
      html_node(node) %>% 
      # Extract the link
      html_attr("href")
    
    #adjust counters if a new box is reached
    if (is.na(specific_url[j])) {
      #move onto the next box
      cur_box <- cur_box+2
      #reset counter inside the box
      k <- 1
      #re-iterate over the same element, since it's currently filled as "NA"
      j <- j-1
    }
    
    #increment counters to read the next line
    j <- j+1
    k <- k+1
  }
  
  #line break
  writeLines("\n")
  
  #now it's time to scrape analytics from xtools
  #initialize arrays to scrape analytics about the page
  edit_count <- character(length = (length(cast)))
  num_editors <- character(length = (length(cast)))
  edits_by_top_editors <- character(length = (length(cast)))
  word_count <- character(length = (length(cast)))
  reverted_edits <- character(length = (length(cast)))
  
  #progress bar :)
  pb2  <- txtProgressBar(1, length(cast), style=3)
  writeLines("Scraping analytics\n")
  
  #scrape analytics
  for(j in 1:length(cast)){
    setTxtProgressBar(pb2, j)
    #remove "/wiki" from each url
    cur_url <- gsub("/wiki", "", specific_url[j])
    #create url towards analytics page
    pg_stats <- paste("https://xtools.wmflabs.org/articleinfo/en.wikipedia.org", cur_url, sep="")
    #if there is not a page for the article, mark its data as "NA"
    if(grepl("/w/index.php?", pg_stats)){
      edit_count[j] <- NA
      num_editors[j] <- NA
      edits_by_top_editors[j] <- NA
      word_count[j] <- NA
      reverted_edits[j] <- NA
    }
    
    #read data from analytics page into tables
    else{
        pg2 <- read_html(pg_stats)
        edit_count[j] <- trimws(html_text(html_nodes(pg2, ".col-lg-5 tr:nth-child(4) td+ td")))
        num_editors[j] <- trimws(html_text(html_nodes(pg2, ".col-lg-5 tr:nth-child(5) td+ td")))
        edits_by_top_editors[j] <- trimws(html_text(html_nodes(pg2, "tr:nth-child(11) .stat-list--new-group+ .stat-list--new-group")))
        word_count[j] <- trimws(html_text(html_nodes(pg2, ".col-lg-3 tr:nth-child(3) td+ td")))
        reverted_edits[j] <- trimws(html_text(html_nodes(pg2, ".col-lg-6 tr:nth-child(5) td+ td")))
        
    }
  }
  
  #line break
  writeLines("\n")
  
  #Create char array of years to attach to data frame
  year <- character(length = (length(cast)))
  for(j in 1:length(cast)){
    year[j] <- i+1900
  }
  
  
  #Compile lists into data frame
  data.frame(title, director, cast, genre, notes, year, edit_count, num_editors, edits_by_top_editors, reverted_edits, word_count, specific_url)
  
}) -> americanFilms #data frame is written into americanFilms

#Output data frame to csv
write.csv(americanFilms, file = "csv_outputs/films.csv")

#visual summary of output
dplyr::glimpse(americanFilms)