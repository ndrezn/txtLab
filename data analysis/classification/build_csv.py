import pandas
import os
from math import floor
from progress.bar import Bar


# mediums to test on (add 'films' and/or 'novels' and/or 'tv'):
scans = ['films','tv', 'novels']

# set as true to run on the sample data set, false to run on everything
samples = False


# return data frame with genre or year as the label. Label can be either "year" or "genre"
def meta(file_list):
    texts,genres,years_50,mediums,years_25,years = [],[],[],[],[],[]
    meta_src = "/Volumes/KINGSTON/txtlab/out/metadata/"
    meta = {'films':pandas.read_csv(meta_src+'films.csv'),\
             'novels':pandas.read_csv(meta_src+"novels.csv"), \
             'tv':pandas.read_csv(meta_src+'tv2.csv')}
             
    bar = Bar('Processing...', max=len(file_list))

    for file in file_list:
        bar.next()
        medium = file.split('/')[0]
        title = file.split('/')[1]

        if medium not in scans:
            continue

        df = meta[medium]
        url = "/wiki/" + title.split('.')[0]
        if medium == 'tv' or medium == 'films':
            try:
                year = df.loc[df.url == url, 'year'].tolist()[0]
            except IndexError:
                continue
            genre = df.loc[df.url == url, 'genre'].tolist()[0]
            genre = str(genre).lower()        
        else:
            try:
                year = df.loc[df.url == url, 'year'].tolist()[0]
                genre = None
            except IndexError:
                continue
        try:
            year_50 = 50 * floor(year/50)
            year_25 = 25 * floor(year/25)
        except:
            year = None

        genres.append(genre)
        mediums.append(medium)
        years_50.append(year_50)
        years_25.append(year_25)
        years.append(year)


        content = open(directory+file, 'r')
        texts.append(content.read())

    trainDF = pandas.DataFrame()
    trainDF['GENRE'] = genres
    trainDF['YEAR'] = years
    trainDF['YEAR_50'] = years_50
    trainDF['YEAR_25'] = years_25
    trainDF['MEDIUM'] = mediums
    trainDF['TEXT'] = texts

    bar.finish()
    return trainDF

# load the dataset
# directory of jsons to be parsed
if samples:
    directory = "/Volumes/NATHAN/out/changes_as_text/samples/"
else:
    directory = "/Volumes/NATHAN/out/changes_as_text/"

folder_list = [f for f in os.listdir(directory) if not f.startswith('.')]
file_list = []
for folder in folder_list:
    file_list+=([folder+"/"+f for f in os.listdir(directory+folder) if not f.startswith('.')])

trainDF = meta(file_list)
print(trainDF)

trainDF.to_pickle('/Volumes/NATHAN/out/classification_meta/' + 'complete_features.pkl')