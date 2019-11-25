library(rvest)

urls <- read.csv("csv_outputs/novels csvs/novels_urls.csv", header = TRUE)

list_of_urls <- as.vector(urls[,1])

#pb  <- txtProgressBar(2186, length(list_of_urls), style=3)

for (i in 3990:length(list_of_urls)) {
  message(i/length(list_of_urls))
  #setTxtProgressBar(pb, i)
  #create url to access wikipedia page
  url <- paste("https://en.wikipedia.org", list_of_urls[i], sep="")
  
  file_name <- paste("txt_files/novels/", i, ".txt", sep = "")
  file<-file(file_name)
  
  tryCatch(
    {
      pg <- read_html(url)
      text <- html_text(html_nodes(pg, "ul:nth-child(8) li , p"), trim = TRUE)
    },
    error = function(cond) {
    }
  )
  
  writeLines(text, file)
  
  text <- NULL
  
  close(file)
  
}
