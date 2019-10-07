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
from progress.bar import Bar
from multiprocessing import Pool
import timeit


# load json object from file
def read_json(file):
	with open(file, encoding='utf-8', errors='ignore') as json_data:
		d = json.load(json_data)
	return d

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


def edit_sizes(changes):
	sizes = {'Empty': 0, '1-25 words': 0, '26-50 words': 0, '51-75 words': 0, '76+ words': 0}

	# for each differential vector
	for vec in changes:
		edit_size = 0
		for k in vec.items():
			if k[1] is not 0:
				edit_size+= abs(k[1])
		if edit_size > 75:
			sizes['76+ words'] += 1
		elif edit_size > 50:
			sizes['51-75 words'] += 1
		elif edit_size > 25:
			sizes['26-50 words'] += 1
		elif edit_size > 0:
			sizes['1-25 words'] += 1
		elif edit_size is 0:
			sizes['Empty'] += 1
	return sizes


# add together all the additions (positive vector counts) into one counter
# add together all removals (negative vector counts) into another counter
def compile(changes, spam):
	added = Counter()
	removed = Counter()
	const = Counter()

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

	document = Document(added, removed, const, sizes, spam)
	return document


def main():
	genre = "tv"
	# directory of jsons to be parsed
	directory = "/Volumes/KINGSTON/txtlab/jsons/" + genre + "/"
	
	# output for total count
	out = "/Volumes/KINGSTON/txtlab/may-13/" + genre + ".json"
	
	# array to hold jsons for each document

	total = []

	file_list = [f for f in os.listdir(directory) if not f.startswith('.')]
	bar = Bar('Counting...', max=len(file_list))

	for file in file_list:
		# try/except block to make sure only json files are read into the program
		spam = 0

		vecs = []
		# document represents the complete set of revisions
		document = read_json(directory + file)
		# for each revision in the document of revisions
		texts = dict()
		for item in document:
			texts[item['metadata']['revid']] = (item['text']['text'])

		# multiprocess the collections
		pool = Pool(os.cpu_count())	# create a pool
		texts.values() = pool.map(create_collection, texts.values())	# process iterable
		pool.close()

		for parsed in collections:
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
				else:
					spam += 1
		# create list of vectors between each document
		changes = successors(vecs)
		# compile vectors between each document
		compiled = compile(changes, spam)
		# full json of counted words
		total.append(compiled.make_json(file))
		bar.next()
	bar.finish()
	save(out, total)


if __name__== "__main__":
	start = timeit.default_timer()
	main()
	stop = timeit.default_timer()
	print('Time:', stop - start)
