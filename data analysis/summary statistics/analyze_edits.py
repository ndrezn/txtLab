## using the full set of edits, calculates: 
# number of reversions
# top users

import os
import json
from progress.bar import Bar
import timeit
from multiprocessing import Pool
from collections import Counter
from wiki_page import *


def get_documents(directory):
	file_list = [f for f in os.listdir(directory) if not f.startswith('.')]
	total_edits = 0
	spam = 0

	files = [(directory+file) for file in file_list]

	pool = Pool()
	documents = pool.map(read_json, files)	# process iterable
	pool.close()

	return documents


def count_reversions(documents):
	reversions = 0
	human_reversions = 0

	for document in documents:
		for version in document:
			comment = version.comment.lower()
			user = version.user.lower()
			
			if "revert" in comment or "undid" in comment: 
				reversions+=1
				if "bot" not in user and "bot" not in comment:
					human_reversions+=1

	return reversions, human_reversions


def count_users(documents):
	users = Counter()

	for document in documents:
		for version in document:
			users[version.user.lower()] += 1

	return users


def main():
	genres = ['novels', 'films', 'tv']

	for genre in genres:
		print(genre)
		# directory of jsons to be parsed
		directory = "/Volumes/KINGSTON/txtlab/jsons/" + genre + "/"

		documents = get_documents(directory)

		# reversions, human_reversions = count_reversions(documents)

		# print("Human reversions: " + str(human_reversions))
		# print("All reversions: " + str(reversions) + "\n")

		users = count_users(documents)
		print(users.most_common(15))

if __name__ == '__main__':
	start = timeit.default_timer()
	main()
	stop = timeit.default_timer()
	print('Time:', stop - start)
