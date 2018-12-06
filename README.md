# txtLab : Research on Wikipedia

## general
This is a repository for scripts written to collect data on wikipedia articles and lists with the intent of understanding
how language is fought over on Wikipedia. Research is based in collecting lists of articles compiled 
by Wikipedia editors or categories on America novels, TV shows, and films and compiling revisions to individual 
articles included in those lists over time.

The project is being conducted for the McGill [txtLab](https://txtlab.org/).

## this repository
Included in this repository are scripts written in Python and R used to collect information on Wikipedia entries.
Lists were first scraped using R into CSVs with metadata on each article, including edit count, editors
involved, URLs, and other data. Output CSV sheets created on November 14th, 2018 are available in the repository.

Python scripts were written to track changes to specific articles over time. edit_histories.py is a script which, 
given any Wikipedia article, will output every version of the article as a text file and output metadata on each revision
as a seperate text file. Metadata includes the user who made the edit, the revision ID which can be used to access
the specific article, comments associated with an edit, words added, and words removed.

edit_histories.py uses MWClient to collect information from the Wikipedia API on a given article.

## data usage
Data collected from these scripts will be used to understand language frequently removed and added to Wikipedia
and track language associated with different content assesments to judge "good" and "bad" language judged by
Wikipedia editors, as well as understanding and answering other questions on how language works and changes over
time on the encyclopedia.
