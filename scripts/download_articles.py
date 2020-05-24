'''
Download a list of articles as specified by a CSV
'''

import wikipedia_histories
import pandas as pd
from progress.bar import IncrementalBar

sample = pd.read_csv('./subsample_depth_3.csv')
sample = sample.loc[sample['Domain'] == 'politics'][387:]

bar = IncrementalBar('Downloading articles... ', max=len(sample))


for page, domain in zip(sample['Pages'], sample['Domain']):
	bar.next()

	try:
		cur = wikipedia_histories.get_history(page)

		df = wikipedia_histories.build_df(cur)

		df.to_csv("./out/"+domain+"/"+page+'.csv')
	except Exception as e:
		print(e)
	

bar.finish()