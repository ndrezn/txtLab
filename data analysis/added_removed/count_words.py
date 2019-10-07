## takes input as a set of jsons of page histories for wiki articles
## converts the set of revisions to a type Document()
## this gives a list of total added, removed, and constant words
## and their counts. Then takes the ratio of each added, removed, const. to the
## totals and outputs the entire object as a json file.

import json
from document_class import *
from collections import Counter
import re
import os
import json


# load json object from file
def read_json(file):
	with open(file) as json_data:
		d = json.load(json_data)
	return d


# save json object out
def create(path, counter):
	with open(path, 'w') as outfile:
		json.dump("{", outfile)
	with open(path, 'a') as outfile:
		json.dump(counter, outfile)

# save json object out
def save(path, counter):
	with open(path, 'w') as outfile:
		json.dump(counter, outfile)


#create vector of word counts for a single document
def create_collection(document):
	c = Counter(
		# set to lower case
		word.lower()
		# remove punctuation
		for word in re.findall(r'\b[^\W\d_]+\b', document))
	return c


# create an array of differential vectors representing 
# changes between each page
def successors(document):
	prev = Counter()

	changes = []
	for cur in document:
		# copy current document
		temp = Counter(cur)
		# subtract the previous document from the current document
		temp.subtract(prev)
		# add the differential vector to an array
		changes.append(temp)
		# iterate the previous document
		prev = cur
	return changes


# add together all the additions (positive vector counts) into one counter
# add together all removals (negative vector counts) into another counter
def compile(changes):
	added = Counter()
	removed = Counter()
	const = Counter()

	# for each differential vector
	for vec in changes:
		# for each (word, count) tuple in the vector
		for k in vec.items():
			# if the count is positive (added word) increase count for that
			# word by the count in the vector
			if k[1] > 0:
				added[k[0]] += k[1]
			# if count is negative ...
			elif k[1] < 0:
				removed[k[0]] -= k[1]

			else:
				const[k[0]] += 1

	document = Document(added, removed, const)

	return document


def main():
	genre = "films"
	# directory of jsons to be parsed
	directory = "/Volumes/NATHAN/out/complete_articles/" + genre + "/"
	
	# output for total count
	out = "/Volumes/NATHAN/out/complete_articles/as_document/" + genre + ".json"

	# created = False
	total = []
	for file in os.listdir(directory):
		# try/except block to make sure only json files are read into the program
		if file.endswith('.json'):
			print(file)
			vecs = []
			# document represents the complete set of revisions
			document = read_json(directory + file)
			# for each revision in the document of revisions
			for item in document:
				# create list out of text to test token/type
				parsed = create_collection(item['text']['text'])
				# counters
				unique_words = 0
				total_words = 0
				# get the number of unique words and total number of words
				for word in parsed.items():
					unique_words += 1
					total_words += word[1]
				# if there is content in the text
				if unique_words > 0:
					# check that type_token ratio is above 10%
					if unique_words/total_words > .1:
						# create a counter for the document
						vecs.append(parsed)
			# create list of vectors between each document
			changes = successors(vecs)
			# compile vectors between each document
			compiled = compile(changes)
			# full json of counted words
			total+=compiled.make_json(file)
			# if created is False:
			# 	create(out, compiled.make_json(file))
			# 	created = True
			# else:
			# 	save(out, compiled.make_json(file))
	
	save(out, total)

if __name__== "__main__":
	main()
