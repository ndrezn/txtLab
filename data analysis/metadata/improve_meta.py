import pandas as pd
from wiki_page import *
from datetime import datetime,date,time
from progress.bar import Bar
from statistics import mean

# number of human and bot reversions to the page
def count_reversions(document):
	reversions = 0
	human_reversions = 0

	for version in document:
		comment = version.comment.lower()
		user = version.user.lower()
		
		if "revert" in comment or "undid" in comment: 
			reversions+=1
			if "bot" not in user and "bot" not in comment:
				human_reversions+=1

	return reversions, human_reversions


# number of edits to the page
def count_edits(document):
	return len(document)


# dict of users and number of edits they contributed to the pate
def count_users_and_ratings(document):
	users = {}
	ratings = {}
	times = []
	for version in document:
		user = version.user.lower()
		rating = version.rating.lower()

		if user not in users:
			users[user] = 1
		else:
			users[user] += 1
		if rating not in ratings:
			ratings[rating] = 1
			times.append(datetime.strptime(version.time, "%Y-%m-%d %H:%M:%S"))
		else:
			ratings[rating] +=1

	counted_times = []
	if len(times) > 1:
		fst = times.pop(0)

		for cur in times:
			diff = abs((fst-cur).total_seconds())
			diff = diff/3600
			counted_times.append(diff)
			fst = cur
		avg_time = mean(counted_times)
	else:
		avg_time = None

	return users,(ratings, avg_time)


# average time between each edit
def average_time(document):
	datetimes = [datetime.strptime(version.time, "%Y-%m-%d %H:%M:%S") for version in document]
	if len(datetimes) < 2:
		return None, None
	fst = datetimes.pop(0)
	
	total_time = 0
	total_short_edits = 0
	num_short_edits = 0

	for cur in datetimes:
		diff = abs((fst-cur).total_seconds())
		diff = diff/3600

		if diff < 720:
			total_short_edits += diff
			num_short_edits +=1

		total_time += diff
		fst = cur

	avg = ((total_time/len(datetimes)))
	if num_short_edits < 2:
		return avg, None
	else:
		avg_short = ((total_short_edits/num_short_edits))
	return avg,avg_short


def total_minor(document):
	minor = 0
	for version in document:
		minor+=int(version.kind)
	return minor

def main():
	genres = ['films', 'novels', 'tv']
	meta = {}

	for genre in genres:
		meta[genre] = pd.read_csv("/Volumes/NATHAN/out/metadata/" + genre + ".csv")


	directory = "/Volumes/NATHAN/out/complete_articles/all/"

	folder_list = [directory + f for f in genres]
	file_list = []
	for folder in folder_list:
		file_list+=([folder+"/"+f for f in os.listdir(folder) if not f.startswith('.')])

	reverts,edits,usr_rtg_rtgtime,avg_time,minor,titles,mediums,genres,years=[],[],[],[],[],[],[],[],[]
	
	bar = Bar('Processing...', max=len(file_list))
	for file in file_list:
		bar.next()
		content = file.split('/')
		medium = list(reversed(content))[1]
		title = list(reversed(content))[0].split('.')[0]

		df = meta[medium]
		url = "/wiki/" + title

		cur = read_json(file)

		if medium == 'tv' or medium == 'films':
			try:
				genre = df.loc[df.url == url, 'genre'].tolist()[0]
				year = df.loc[df.url == url, 'year'].tolist()[0]
			except IndexError:
				continue
			genre = str(genre).lower()		
		else:
			try:
				year = df.loc[df.url == url, 'year'].tolist()[0]
				genre = None
			except IndexError:
				continue

		reverts.append(count_reversions(cur))
		edits.append(count_edits(cur))
		usr_rtg_rtgtime.append(count_users_and_ratings(cur))
		avg_time.append(average_time(cur))
		minor.append(total_minor(cur))
		titles.append(title)
		mediums.append(medium)
		genres.append(genre)
		years.append(year)
	
	bar.finish()

	reverts,human_reverts=zip(*reverts)
	users,ratingstimes=zip(*usr_rtg_rtgtime)
	ratings, rating_times = zip(*ratingstimes)
	avg_time,avg_time_short = zip(*avg_time)
	complete = pd.DataFrame({'title':titles, 'medium':mediums, 'year':years,'genre':genres,'edits':edits, \
		'users':users,'ratings':ratings,'reverts':reverts,'human_reverts':human_reverts, \
		'rating_times': rating_times, 'avg_time':avg_time, 'avg_time_short':avg_time_short,'minor':minor})

	complete.to_pickle("/Volumes/NATHAN/out/metadata/improved_meta/complete2.pkl")

main()