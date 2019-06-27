## takes as input a compiled set of changes
## outputs the top words as a CSV file
## also offers a method to output as a word cloud

import json
from document_class import *
from collections import Counter
import csv
import pandas as pd
import wordcloud
import matplotlib.pyplot as plt


def out(added, removed, path):
	with open(path + "added.csv", 'w') as f:
		writer = csv.writer(f)
		writer.writerow(['word', 'addition count'])
		for row in added.items():
			writer.writerow(row)
	with open(path + "removed.csv", 'w') as f:
		writer = csv.writer(f)
		writer.writerow(['word', 'removal count'])
		for row in removed.items():
			writer.writerow(row)


def top_out(counts, path, genre):
	df = pd.DataFrame(counts)
	df.to_csv(path + genre + "_changes.csv")


def word_cloud_out(data, out):
	data = dict(data)
	cleaned = dict()
	
	stopwords = set(wordcloud.STOPWORDS)
	stopwords = stopwords.union(['mw', 'parser', 'penis', 'dick', 's', 'fuck', 'gay', 'xd', 
								 'cocks', 'eeeeeeeeeewwwwwwwwwwwaaaaaaaaaaa', 'lol', 'hi',
								 "svg", 't', 'niggers', 'output', 'jpg', 'cite', 'ref'])
	for key,value in zip(data.keys(), data.values()):
		if key not in stopwords:
			cleaned[key]=value

	cloud = wordcloud.WordCloud(width=2000, 
					  height=1000,
					  background_color="white",
					  max_words = 40)

	cloud.generate_from_frequencies(cleaned)
	cloud.to_file(out)


def count_certain_words(document):
	posessive = ['I', 'me', 'myself']
	snd_pers = ['you', 'yourself', 'your', 'yours']
	female = ['she', 'her', 'hers']
	male = ['he', 'him', 'his']
	neutral = ['they', 'them', 'theirs']




def create_g_word_cloud(genre):
		# output word clouds for the g-squared using either changes or constant as reference text
		g_squared = document.g_squared_const()
		out_g = "/Users/nathandrezner/OneDrive - McGill"\
				" University/McGill/txt Lab/out/changes/visuals/g_squared/"\
				"no_stopwords/const as analysis text/" + genre + ".png"
		word_cloud_out(Counter(g_squared).most_common(100), out_g)
		
		g_squared = document.g_squared_changes()
		out_g = "/Users/nathandrezner/OneDrive - McGill"\
				" University/McGill/txt Lab/out/changes/visuals/g_squared/"\
				"no_stopwords/changes as analysis text/" + genre + ".png"
		word_cloud_out(Counter(g_squared).most_common(100), out_g)


def create_word_cloud(genre):	
	out_cloud = "/Users/nathandrezner/OneDrive - McGill University/"\
 			"McGill/txt Lab/out/changes/visuals/" + genre + "/"
	count = 300

	word_cloud_out(document.added.most_common(count), (out_cloud+"added.png"))
	print("Done added cloud.")
	word_cloud_out(document.removed.most_common(count), (out_cloud+"removed.png"))
	print("Done removed cloud.")
	word_cloud_out(document.const.most_common(count), (out_cloud+"constant.png"))
	print("Done constant cloud.")


def main():
	genres=['novels' ,'tv', 'films']

	for genre in genres:
		print("\n" + genre)
		document = read_json("/Volumes/KINGSTON/txtlab/may-13/"+genre+".json")
		document.print()
		# sizes = [k[1] for k in document.sizes.items()]
		# labels = [k[0] for k in document.sizes.items()]

		# plt.pie(sizes, labels=labels,
		# 		autopct='%1.1f%%', shadow=True, startangle=140)

		# plt.axis('equal')
		# plt.show()

		# out_csv = "/Users/nathandrezner/OneDrive - McGill University/McGill/txt Lab/"\
		# 		  "out/changes/complete/changes/csvs/" + genre

		# document.simple_csv(out_csv)




if __name__== "__main__":
	main()
