import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv('/Users/ndrezn/OneDrive - McGill University/Github/txtLab/results/category_csvs/sampler_3.csv')
df2 = pd.read_csv('/Users/ndrezn/OneDrive - McGill University/Github/txtLab/results/category_csvs/culture_3.csv')

df = pd.concat([df, df2])


cats = ['sciences', 'sports', 'politics', 'culture']
lens2 = []
for j in range(0, 4):
	lens = []
	for i in range (0, 4):
		lens.append(len(df.loc[(df['Level']==i) & (df['Domain'] == cats[j])].reset_index(drop=True)))
	lens2.append(len(df.loc[df['Level']==j].reset_index(drop=True)))

ax = sns.lineplot(y=lens2, x=list(range(0,4)))
plt.xlabel('Level', fontsize=10)
plt.ylabel('Article count', fontsize=10)
plt.title('Article count by category depth')# ('+cats[j]+')')
plt.show()


# df = pd.read_csv('/Users/ndrezn/OneDrive - McGill University/Github/txtLab/results/category_csvs/subsample_3.csv')

# print(len(df.loc[df['Relevant?']==1].reset_index(drop=True)))
# print(len(df))