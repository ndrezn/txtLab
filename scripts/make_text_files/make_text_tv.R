library(rvest)

urls <- read.csv("csv_outputs/tv csvs/tv_urls.csv", header = TRUE)

list_of_urls <- as.vector(urls[,1])

pb  <- txtProgressBar(1, length(list_of_urls), style=3)

for (i in 1:length(list_of_urls)) {
  setTxtProgressBar(pb, i)
  #create url to access wikipedia page
  url <- paste("https://en.wikipedia.org", list_of_urls[i], sep="")
  
  file_name <- paste("txt_files/tv/", i, ".txt", sep = "")
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
