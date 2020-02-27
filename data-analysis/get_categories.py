import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import wikipediaapi

data_dir = '../results/data/' 
directory_files = [
			f for f in os.listdir(data_dir) if not f.startswith(".")
]


# sciences = ['Category:Branches_of_biology', 'Category:Fields_of_mathematics', 'Category:Concepts_in_physics', 'Category:Chemistry']

# sports = ['Category:Ice_hockey_in_the_United_States', 'Category:American_football_in_the_United_States', 'Category:Basketball_in_the_United_States', 'Category:Baseball_in_the_United_States']
culture = ['Category:Television_in_the_United_States', 'Category:American_films', 'Category:American_novels']
# politics = ['Category:Conservatism_in_the_United_States', 'Category:Liberalism_in_the_United_States']

domains = {'culture':culture}#'sciences':sciences, 'sports':sports, 'politics':politics,}# 

def get_pages_of_cat(category, categorymembers, dict_of_cats, level=0, max_level=3):
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
    
    category_df = pd.DataFrame()
    
    for category in domains[domain]:
        print(category)
        cat = wiki.page(category)
        try:
            d = get_pages_of_cat(category, cat.categorymembers, {})
        except:
            print('Broken: ' + category)
            continue
        #print(d)
        for subcat in d:
            subcat_df = pd.DataFrame()
            subcat_df['Pages'] = [val[0] for val in d[subcat]]
            subcat_df['Level'] = [val[1] for val in d[subcat]]
            subcat_df['Subcategory'] = subcat
            subcat_df['Category'] = category
            subcat_df['Domain'] = domain
            category_df = pd.concat([category_df, subcat_df])

    full_df = pd.concat([full_df, category_df])

full_df.reset_index(inplace=True, drop=True)
full_df.to_csv('/Users/ndrezn/OneDrive - McGill University/Github/txtLab/results/category_csvs/culture_3.csv')
print(len(full_df))
sampled = pd.DataFrame()

levels = range(0, 4)

for domain in domains:
    for level in levels:
        new = pd.DataFrame()
        new = full_df.loc[(full_df['Level'] == level) & (full_df['Domain'] == domain)]
        try:
            new.sample(n=20, replace=False, random_state=1, inplace=True)
        except:
            continue
        sampled = pd.concat([sampled, new])


sampled.reset_index(drop=True, inplace=True)
sampled.sort_values(by=['Level', 'Category'], inplace=True)
sampled.to_csv('/Users/ndrezn/OneDrive - McGill University/Github/txtLab/results/category_csvs/culture_3_sub.csv')

