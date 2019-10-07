## counts the number of words added to each wiki page
## compiles the set as a text file and outputs the bag of words representation 
## of all the added words for each page

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


# add together all the additions (positive vector counts) into one counter
# add together all removals (negative vector counts) into another counter
def compile(changes):
	added = Counter()
	for vec in changes:
		# for each (word, count) tuple in the vector
		for k in vec.items():
			# if the count is positive (added word) increase count for that
			# word by the count in the vector
			if k[1] > 0:
				added[k[0]] += k[1]

	return added


def main():
	# directory of jsons to be parsed
	directory = "/Volumes/NATHAN/out/films/"
	
	# output for total count
	out = "/Volumes/NATHAN/out/changes_as_text/films/"
	
	# array to hold jsons for each document

	total = []

	folder_list = [f for f in os.listdir(directory) if not f.startswith('.')]
	file_list = []
	for folder in folder_list:
		file_list+=([folder+"/"+f for f in os.listdir(directory+folder) if not f.startswith('.')])

	bar = Bar('Counting...', max=len(file_list))

	for file in file_list:
		vecs = []
		# document represents the complete set of revisions
		document = read_json(directory + file)
		# for each revision in the document of revisions
		texts = []
		for item in document:
			texts.append(item['text']['text'])

		# multiprocess the collections
		pool = Pool(os.cpu_count())	# create a pool
		collections = pool.map(create_collection, texts)	# process iterable
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
					continue
		# create list of vectors between each document
		changes = successors(vecs)
		# compile vectors between each document
		compiled = compile(changes)
		# full json of counted words
		string = ''
		for key,value in compiled.items():
			i = 0
			while i < value:
				string += key + ' '
				i += 1
		outfile = open(out + os.path.splitext(file)[0].split('/')[1] + '.txt', 'w+')
		outfile.write(string)
		outfile.close
		bar.next()
	bar.finish()


if __name__== "__main__":
	start = timeit.default_timer()
	main()
	stop = timeit.default_timer()
	print('Time:', stop - start)
