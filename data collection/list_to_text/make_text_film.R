library(rvest)

full_list <- read.csv("csv_outputs/films.csv", header = TRUE)

list_of_titles <- as.vector(full_list[,2])

for (i in 1:length(list_of_titles)) {
  #progress indicator
  if (i%%10 == 0){
    message("Completed: ", round(100*(i/length(list_of_titles)), digits=2), "%")
  }
  
  #create url to access wikipedia page
  url <- paste("https://en.wikipedia.org", full_list[i, 8], sep="")
  
  file_name <- paste("txt_files/films/", i, ".txt", sep = "")
  file<-file(file_name)
  
  metadata <- c(paste("url = " , url, sep = ""),
                paste("id = ", i, sep = ""),
                paste("title = ", full_list[i,2], sep = ""),
                paste("director = ", full_list[i, 3], sep = ""),
                paste("cast = ", full_list[i, 4], sep = ""),
                paste("genre = ", full_list[i, 5], sep = ""), 
                paste("notes = ", full_list[i, 6], sep = ""), 
                paste("year = ", full_list[i, 7]), sep = "")

  tryCatch(
    {
      pg <- read_html(url)
      text <- html_text(html_nodes(pg, "ul:nth-child(8) li , p"), trim = TRUE)
    },
    error = function(cond) {
    }
  )
  
  writeLines(c(metadata, text), file)
  
  text <- NULL
  
  close(file)
  
}
