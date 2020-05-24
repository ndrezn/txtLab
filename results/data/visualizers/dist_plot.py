import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


palette = ['#80d3dc', '#f9a43f', '#fde28b', '#ec1b30']
palette = sns.color_palette(palette)


df = pd.read_csv('./results/data-sets/category-sampling/numerical_metadata.csv')
df['Edits per user'] = df['Total edits']/df['Number of unique editors']

ax = sns.pairplot(df, hue='domain')
plt.show()