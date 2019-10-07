import json
import re


def read_json(file):
	with open(file) as json_data:
		d = json.load(json_data)
	return d


def find_pages(document, word):
	document = document.pop()
	for item in document:
		print(item)
		for a,b in zip(dict(item['added']).keys(), dict(item['added']).values()):
			if a == word:
				print((item['title'] + ": ").ljust(50) + str(b))


def find_revisions(document, term):
	counts = dict()
	for version in document:
		j = 0
		for word in re.findall(r'\b[^\W\d_]+\b', version['text']['text']):
			if word.lower() == term:
				j+=1
		if j > 0:
			counts[version['metadata']['revid']] = j
	return counts


def print_counts(document, word):
	counts = find_revisions(document, word)
	for a,b in zip(counts.keys(), counts.values()):
		print(str(a) + ": " + str(b))


def main():
	word = "illustrating"
	page = "Roll_of_Thunder,_Hear_My_Cry.json"
	genre = "novels"

	# compiled set of all changes
	document = read_json("/Volumes/NATHAN/out/complete_articles/as_document/" + genre + ".json")
	# metadata json file for a page
	#page = read_json("/Users/dh_lab_03/Desktop/nathan/jsons/" + genre + "/" + page)
	
	find_pages(document, word)
	print()
	#print_counts(page, word)	


if __name__== "__main__":
	main()