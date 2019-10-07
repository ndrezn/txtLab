import pandas as pd

def read_pickle_file(file):
    pickle_data = pd.read_pickle(file)
    return pickle_data

df = read_pickle_file("/Volumes/NATHAN/out/metadata/improved_meta/complete.pkl")

df = df[['title', 'medium', 'year', 'avg_time','avg_time_short']]
df.to_csv("/Volumes/NATHAN/out/metadata/improved_meta/time_csv.csv")