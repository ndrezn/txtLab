import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


x = 'Average deleted words'


paper = ['#80d3dc', '#f9a43f', '#fde28b', '#ec1b30']

paper = sns.color_palette(paper)

sns.set(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})

df = pd.read_csv('./results/data-sets/category-sampling/numerical_metadata.csv')
df['Edits per user'] = df['Total edits']/df['Number of unique editors']


# df = df.groupby('domain').mean()
# df.to_csv('~/Desktop/test.csv')

# df = df.loc[df[x] < 10]

# Initialize the FacetGrid object
pal = sns.cubehelix_palette(10, rot=-.25, light=.7)
g = sns.FacetGrid(df, row="domain", hue="domain", aspect=15, height=.5, palette=paper)

# Draw the densities in a few steps
g.map(sns.kdeplot, x, clip_on=False, shade=True, alpha=1, lw=1.5, bw=.2)
g.map(sns.kdeplot, x, clip_on=False, color="w", lw=2, bw=.2)
g.map(plt.axhline, y=0, lw=2, clip_on=False)


# Define and use a simple function to label the plot in axes coordinates
def label(x, color, label):
    ax = plt.gca()
    ax.text(0, .2, label, fontweight="bold", color=color,
            ha="left", va="center", transform=ax.transAxes)


g.map(label, x)

# Set the subplots to overlap
g.fig.subplots_adjust(hspace=-.25)

# Remove axes details that don't play well with overlap
g.set_titles("")
g.set(yticks=[])
g.despine(bottom=True, left=True)
plt.show()