'''
Based on a set of downloaded articles represented as CSV's, generate a metadata for those articles.
'''

import pandas as pd
import os
from statistics import mean
import time


fpath = 'results/data-sets/category-sampling/'
domains = ['culture', 'politics', 'sciences', 'sports']


start = time.time()
def get_time_diff(prev_time, cur_time):
	if prev_time == None:
		prev_time = cur_time
		return 0
	else:
		time_diff = cur_time-prev_time

	return time_diff.total_seconds()/3600


def get_diffs(df):
	addition_lengths = []
	deletion_lengths = []
	time_diffs = []
	prev_count = 0
	prev_time = None

	prev_quality = str(df.iloc[0]['Rating']).strip().lower()
	prev_quality_time = df.iloc[0]['Time']
	rating_change_times = []

	for i, row in df.iterrows():
		
		word_count = len(str(row['Content']).split())
		
		if word_count < prev_count:
			deletion_lengths.append(prev_count-word_count)
		else:
			addition_lengths.append(word_count-prev_count)

		prev_count = word_count

		cur_time = row['Time']
		time_diff = get_time_diff(prev_time, cur_time)
		time_diffs.append(time_diff)
		prev_time = cur_time


		if str(row['Rating']).strip().lower() != prev_quality or i == len(df)-1:
			time_to_change = get_time_diff(prev_quality_time, cur_time)
			rating_change_times.append(time_to_change)
			prev_quality_time = cur_time
			prev_quality = str(row['Rating']).strip().lower()

	age = get_time_diff(df.iloc[0]['Time'], df.iloc[len(df)-1]['Time'])

	if not deletion_lengths:
		return mean(addition_lengths), 0, mean(time_diffs), mean(rating_change_times), age
	return mean(addition_lengths), mean(deletion_lengths), mean(time_diffs), mean(rating_change_times), age


meta = []
global_ratings = []
for domain in domains:
	ratings = {'domain':domain}
	cur = fpath+domain+"/"

	for f in os.listdir(cur):
		df = pd.read_csv(cur+f)
		df['Time'] = df['Time'].apply(pd.to_datetime)
		length = len(df)

		try:
			addition_length, deletion_length, time_diff, rating_change_time, age = get_diffs(df)
		except:
			continue

		editor_count = len(df['User'].unique())
		row = {'title':f.split('.')[0], 'domain':domain, 'Total edits':length, 'Average added words':addition_length, 'Average deleted words':deletion_length, 'Average time between edits (hours)':time_diff, 'Average time between rating changes (hours)':rating_change_time, 'Article age (hours)':age, 'Number of unique editors':editor_count}
		meta.append(row)

		cur_ratings = df['Rating'].value_counts()

		for rating in cur_ratings.keys():
			try:
				ratings[str(rating).strip().lower()] += cur_ratings[rating]
			except:
				ratings[str(rating).strip().lower()] = cur_ratings[rating]
	global_ratings.append(ratings)

df = pd.DataFrame(meta)
df.to_csv('results/data-sets/category-sampling/numerical_metadata.csv')

ratings = pd.DataFrame(global_ratings)
ratings.to_csv('results/data-sets/category-sampling/ratings_by_domain.csv')


print('It took', time.time()-start, 'seconds.')