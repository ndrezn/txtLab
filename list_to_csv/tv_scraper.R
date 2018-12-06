library(rvest)

urls <- read.csv("csv_outputs/tv csvs/tv_urls.csv", header = TRUE)
titles <- read.csv("csv_outputs/tv csvs/tv_titles.csv", header = TRUE)

#scrape analytics from xtools
#initialize arrays to scrape analytics about the page
edit_count <- character()
num_editors <- character()
edits_by_top_editors <- character()
word_count <- character()
reverted_edits <- character()

#progress bar :)
pb  <- txtProgressBar(1, 2487, style=3)
writeLines("Scraping analytics\n")

#scrape analytics
for(i in 1:2487){
  
  setTxtProgressBar(pb, i)
  
  #remove "/wiki" from each url
  cur_url <- gsub("/wiki", "", urls[i,1])
  
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

out <- data.frame(titles, urls, edit_count, num_editors, edits_by_top_editors, word_count, reverted_edits)

write.csv(out, file = "csv_outputs/metadata/tv_shows.csv")

