# txtLab : Research on Wikipedia

## General
This is a repository for scripts written to collect data on wikipedia articles and lists with the intent of understanding
how language is fought over on Wikipedia. Research is based in collecting lists of articles compiled 
by Wikipedia editors or categories on America novels, TV shows, and films and compiling revisions to individual 
articles included in those lists over time.

The project is being conducted for the McGill [txtLab](https://txtlab.org/).

## This repository
Included in this repository are scripts written in Python and R used to collect information on Wikipedia entries.

## Data analysis
### Metadata analysis
Generators for different metadata features of the articles. 

analyze_meta generates information about the csv file containing complete data.

improve_meta builds the csv based on seperate information

one_way_anova and tukey_hsd both compute ANOVA testing on times between edits for different medias.

edit_histories.py uses MWClient to collect information from the Wikipedia API on a given article.

### Social networks

Generates randomized social networks representing the user base of different Wikipedia articles using the raw dataset.

### Classifiers
Classifier designed to compare edits in different spaces to each other and predict which space a given article belongs to based on those edits.

The classifier also determines the most distinctive features of each space based on these edits.

## Data collection
There are several data collectors in this repository. scrape_complete.py will download complete histories of given wikipedia pages asychornously and save each page as a json file with a structure represenging the different elements of the page. Other scrapers will download information from Wikipedia lists representing different cultural domains.

