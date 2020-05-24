import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('~/Documents/Github/txtLab/results/data-sets/social-networks/metadata.csv')

sns.set_palette(sns.color_palette("YlGn", 10))

ax = sns.boxplot(data=df, x='kind', y='assortativity')

plt.show()