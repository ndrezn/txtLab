library(rvest)

urls <- read.csv("csv_outputs/novels csvs/novels_urls.csv", header = TRUE)
titles <- read.csv("csv_outputs/novels csvs/novels_titles.csv", header = TRUE)
years <- read.csv("csv_outputs/novels csvs/novels_years.csv", header = TRUE)

list_of_urls <- as.vector(urls[,1])
list_of_years <- as.vector(years[,1])
list_of_titles <- as.vector(titles[,1])



#scrape analytics from xtools
#initialize arrays to scrape analytics about the page
edit_count <- character(length(list_of_urls))
num_editors <- character(length(list_of_urls))
edits_by_top_editors <- character(length(list_of_urls))
word_count <- character(length(list_of_urls))
reverted_edits <- character(length(list_of_urls))

#progress bar :)
pb  <- txtProgressBar(1, length(list_of_urls), style=3)

sheet_length=100
#scrape analytics
for(i in 1:length(list_of_urls)){
  
  setTxtProgressBar(pb, i)
  
  #remove "/wiki" from each url
  cur_url <- gsub("/wiki", "", list_of_urls[i])
  
  #create url towards analytics page
  pg_stats <- paste("https://xtools.wmflabs.org/articleinfo/en.wikipedia.org", cur_url, sep="")
  
  if(grepl("/w/index.php?", pg_stats)){
    edit_count[i] <- NA
    num_editors[i] <- NA
    edits_by_top_editors[i] <- NA
    word_count[i] <- NA
    reverted_edits[i] <- NA
  }
  
  #read data from analytics page into tables
  else{
    pg <- read_html(pg_stats)
    edit_count[i] <- trimws(html_text(html_nodes(pg, ".col-lg-5 tr:nth-child(4) td+ td")))
    num_editors[i] <- trimws(html_text(html_nodes(pg, ".col-lg-5 tr:nth-child(5) td+ td")))
    edits_by_top_editors[i] <- trimws(html_text(html_nodes(pg, "tr:nth-child(11) .stat-list--new-group+ .stat-list--new-group")))
    word_count[i] <- trimws(html_text(html_nodes(pg, ".col-lg-3 tr:nth-child(3) td+ td")))
    reverted_edits[i] <- trimws(html_text(html_nodes(pg, ".col-lg-6 tr:nth-child(5) td+ td")))
  }
  
}

file_name <- "csv_outputs/metadata/novels.csv"
out <- data.frame(list_of_titles, list_of_years, list_of_urls, edit_count, num_editors, edits_by_top_editors, word_count, reverted_edits)
write.csv(out, file = file_name)
