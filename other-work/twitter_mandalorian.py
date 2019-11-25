import jsonlines
import pandas as pd

df = pd.DataFrame(columns=['Author', 'Time', 'URL', 'Favorites', 'Retweets', 'Verified', 'Text'])

with jsonlines.open('/Users/ndrezn/OneDrive - McGill University/Github/txtLab/other work/mandalorian_replies.jsonl') as reader:
    for i,tweet in enumerate(reader):
    	try:
    		df.loc[i] = [tweet['user']['screen_name'], tweet['created_at'], tweet['id'], tweet['favorite_count'], tweet['retweet_count'], tweet['user']['verified'], tweet['full_text']]
    	except:
    		continue


df.to_csv('/Users/ndrezn/OneDrive - McGill University/Github/txtLab/other work/tweets.csv')