'''
Given a set of categories representing domains, gather the articles emcompassed by those categories
'''

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import wikipediaapi

data_dir = '../results/data/' 
directory_files = [
			f for f in os.listdir(data_dir) if not f.startswith(".")
]


sciences = ['Category:Branches_of_biology', 'Category:Fields_of_mathematics', 'Category:Concepts_in_physics', 'Category:Chemistry']
sports = ['Category:Ice_hockey_in_the_United_States', 'Category:American_football_in_the_United_States', 'Category:Basketball_in_the_United_States', 'Category:Baseball_in_the_United_States']
culture = ['Category:Television_in_the_United_States', 'Category:American_films', 'Category:American_novels']
politics = ['Category:Conservatism_in_the_United_States', 'Category:Liberalism_in_the_United_States']

domains = {'sciences':sciences, 'sports':sports, 'culture':culture, 'politics':politics}
def get_pages_of_cat(category, categorymembers, dict_of_cats={}, level=0, max_level=0):
        pages = []
        
        for c in categorymembers.values():
            if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
                dict_of_cats = get_pages_of_cat(c.title, c.categorymembers, dict_of_cats=dict_of_cats, level=level+1, max_level=max_level)
            if "Category:" in c.title:
                continue
            else:
            	pages.append((c.title, level))

        dict_of_cats[category] = pages
        return dict_of_cats

wiki = wikipediaapi.Wikipedia('en')

full_df = pd.DataFrame()
for domain in domains:
    for category in domains[domain]:
        cat = wiki.page(category)
        d = get_pages_of_cat(category, cat.categorymembers)

        category_df = pd.DataFrame()

        for subcat in d:
            subcat_df = pd.DataFrame()
            subcat_df['Pages'] = [val[0] for val in d[subcat]]
            subcat_df['Level'] = [val[1] for val in d[subcat]]
            subcat_df['Subcategory'] = subcat
            category_df = pd.concat([category_df, subcat_df])

    category_df['Category'] = domain
    full_df = pd.concat([full_df, category_df])

full_df.reset_index(inplace=True, drop=True)
full_df.to_csv('/Users/ndrezn/Desktop/item.csv')






# for f in directory_files:
# 	dfs[f.split('.')[0]] = pd.read_csv(data_dir+f)

# sns.distplot(dfs['American television']['length'], kde=True)
# plt.xlabel("Page length (bytes)")
# plt.ylabel("% of articles")
# plt.title("Distribution Article Length (American television)")
# plt.show()