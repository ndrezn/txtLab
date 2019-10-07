# document class for a compiled set of differential vectors.
# represents the added, removed, and constant words over the course of a set of revisions

from collections import Counter
import json
from numpy import log
import csv

 
class Document:
	# counters for each word in the document
	added = Counter()
	removed = Counter()
	const = Counter()
	# number of edits in a document that are spam
	spam = 0
	
	# number of edits that are of certain sizes
	sizes = Counter()

	
	addedAvg = dict()
	removedAvg = dict()
	constAvg = dict()

	# word counts for the document. Order: added, removed, const
	totals = [0, 0, 0]


	def __init__(self, added, removed, const):
		self.added = added
		self.removed = removed
		self.const = const


	def summarize(self):
		# count the total number of added words
		for k in self.added.items():
			self.totals[0] += k[1]

		# count the total number of removed words
		for k in self.removed.items():
			self.totals[1] += k[1]

		# count the total number of constant words
		for k in self.const.items():
			self.totals[2] += k[1]

		# array of counters for words and averages to be calculated
		counters = [self.added, self.removed, self.const]
		averages = [self.addedAvg, self.removedAvg, self.constAvg]
		
		i = 0
		# iterate through each counter and set of averages
		for counter, average in zip(counters, averages):
			# for each key,value pair in the counter
			for k in counter.items():
				# calculate percentage of total that is that word
				average[k[0]] = (k[1] / self.totals[i])
			i += 1

	def make_json(self, title):
		body = {
				"title": title,
				"added": dict(self.added),
				"removed": dict(self.removed),
				"const": dict(self.const),
				"spam": self.spam,
				"sizes": dict(self.sizes)
			}
		return body

	
	# "a" is the number of times the word occurs in the analysis text (added + removed)
	# "b" is the number of times the word occurs in the reference text (constant)
	# "c" is the total number of words in the analysis text. 
	# "d" is the total number of words in the reference text. 
	# E1 = c*(a+b)/(c+d)
	# E2 = d*(a+b)/(c+d)
	# G2 = 2*((a*ln(a/E1)) + (b*ln(b/E2)))
	
	def g_squared_changes(self):
		G2 = dict()

		changes = Counter(self.added) + Counter(self.removed) # a
		c = self.totals[0] + self.totals[1] # c
		d = self.totals[2]

		for word in changes.items():
			a = word[1]
			
			b = self.const[word[0]]
			if b is 0:
				continue

			E1 = c * (a + b) / (c + d)
			E2 = d * (a + b) / (c + d)
			
			G2[word[0]] = 2 * ((a * log(a / E1) + b * log(b / E2)))

		return G2

	def g_squared_const(self):
		G2 = dict()

		d = self.totals[0] + self.totals[1] # c
		c = self.totals[2]

		for word in self.const.items():
			b = word[1]
			
			a = self.added[word[0]] + self.removed[word[0]]
			if a is 0:
				continue

			E1 = c * (a + b) / (c + d)
			E2 = d * (a + b) / (c + d)
			
			G2[word[0]] = 2 * ((a * log(a / E1) + b * log(b / E2)))

		return G2

	def print(self):
		print("Added:")
		print(self.added.most_common(40))
		print("\nRemoved:")
		print(self.removed.most_common(40))
		print("\nConst:")
		print(self.const.most_common(40))
		print("\nSpam:")
		print(self.spam)
		print("\nSizes:")
		print(self.sizes)


	def simple_csv(self, out):
		with open(out+"_added.csv", 'w') as csv_file:
			writer = csv.writer(csv_file)
			for key, value in dict(self.added).items():
				writer.writerow([key, value])

		with open(out+"_removed.csv", 'w') as csv_file:
			writer = csv.writer(csv_file)
			for key, value in dict(self.removed).items():
				writer.writerow([key, value])

		with open(out+"_const.csv", 'w') as csv_file:
			writer = csv.writer(csv_file)
			for key, value in dict(self.const).items():
				writer.writerow([key, value])




# reads a summarized document and returns it as type document, with all pages
# contained in the file compiled together
def read_json(file):
	added = Counter()
	removed = Counter()
	const = Counter()
	sizes = Counter()
	spam = 0
	
	with open(file) as json_data:
		d = json.load(json_data)
	
	for page in d:
		added += page['added']
		removed += page['removed']
		const += page['const']
		spam+=page['spam']
		sizes+=page['sizes']
	
	doc = Document(added, removed, const, sizes, spam)
	doc.summarize()
	return doc


# reads through a json file of wiki pages and returns a requested page summarized
# as a document type
def summarize_document(title, file):
	added = Counter()
	removed = Counter()
	const = Counter()
	
	with open(file) as json_data:
		d = json.load(json_data)
	
	for page in d:
		if page['title'] == title:
			doc = Document(page['added'], page['removed'], page['const'])
	
	doc.summarize()
	return doc

