import wikipedia_histories
import pandas as pd
from progress.bar import IncrementalBar


# full_df = pd.read_csv('./categories_depth_3.csv')

# domains = ['culture', 'sciences', 'sports', 'politics']

# levels = range(0, 4)
# sampled = pd.DataFrame()
# for domain in domains:
#     for level in levels:
#         new = pd.DataFrame()
#         new = full_df.loc[(full_df['Level'] == level) & (full_df['Domain'] == domain)]
        
#         size = min([len(new), 300])

#         new = new.sample(n=size, replace=False, random_state=1)

#         sampled = pd.concat([sampled, new])

# sampled.to_csv('./subsample_depth_3.csv')

sample = pd.read_csv('./subsample_depth_3.csv')


bar = IncrementalBar('Downloading articles... ', max=len(sample))

for page, domain in zip(sample['Pages'], sample['Domain']):

	cur = wikipedia_histories.get_history(page)

	df = wikipedia_histories.build_df(cur)

	df.to_csv("./out/"+domain+"/"+page+'.csv')
	
	bar.next()

bar.finish()