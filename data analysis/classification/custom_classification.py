from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition, ensemble

import pandas, xgboost, numpy, textblob, string
from keras.preprocessing import text, sequence
from keras import layers, models, optimizers
import os
from math import floor

# select either 'medium', 'year', or 'genre'
train_type = 'genre'
# if using train_type as year, then specify the size (in years) to subset films & novels into
base = 25

# mediums to test on (add 'films' and/or 'novels' and/or 'tv'):
mediums = ['films']

# set as true to run on the sample data set, false to run on everything
samples = True


# return data frame with genre or year as the label. Label can be either "year" or "genre"
def meta_as_label(file_list, label):
    texts,labels = [],[]
    meta_src = "/Volumes/KINGSTON/txtlab/out/metadata/"
    meta = {'films':pandas.read_csv(meta_src+'films.csv'),\
             'novels':pandas.read_csv(meta_src+"novels.csv"), \
             'tv':pandas.read_csv(meta_src+'tv2.csv')}
    
    for file in file_list:
        medium = file.split('/')[0]
        title = file.split('/')[1]

        if medium == 'samples' or medium not in mediums:
            continue

        df = meta[medium]
        url = "/wiki/" + title.split('.')[0]
        try:
            cur = df.loc[df.url == url, label].tolist()[0]
        except IndexError:
            continue

        if label is 'year':
            try:
                cur = base * floor(cur/base)
            except:
                cur = 0

        if label is 'genre':
            cur = str(cur).lower()
            if 'animation' in cur:
                cur = 3
            elif 'news' in cur:
                cur = 4
            elif 'reality' in cur:
                cur = 5
            elif 'crime' in cur:
                cur = 6
            elif 'western' in cur:
                cur = 7
            elif 'horror' in cur:
                cur = 8
            elif 'romantic' in cur or 'romance' in cur:
                cur = 9
            elif 'mystery' in cur:
                cur = 10
            elif 'adventure' in cur:
                cur = 11
            
            # most common come last
            elif 'comedy' in cur:
                cur = 0
            elif 'drama' in cur:
                cur = 1
            elif 'action' in cur:
                cur = 2
            else:
                continue


        labels.append(cur)

        content = open(directory+file, 'r')
        texts.append(content.read())

    trainDF = pandas.DataFrame()
    trainDF['text'] = texts
    trainDF['label'] = labels

    return trainDF


#return data frame with medium as the label
def medium_as_label(file_list):
    texts,labels = [],[]
    for file in file_list:
        try:
            content = open(directory+file, 'r')
        except IsADirectoryError:
            continue
        texts.append(content.read())
        labels.append(file.split('/')[0])
    trainDF = pandas.DataFrame()
    trainDF['text'] = texts
    trainDF['label'] = labels

    return trainDF


def part_of_speech_tagging():
    pos_family = {
        'noun' : ['NN','NNS','NNP','NNPS'],
        'pron' : ['PRP','PRP$','WP','WP$'],
        'verb' : ['VB','VBD','VBG','VBN','VBP','VBZ'],
        'adj' :  ['JJ','JJR','JJS'],
        'adv' : ['RB','RBR','RBS','WRB']
    }

    # function to check and get the part of speech tag count of a words in a given sentence
    def check_pos_tag(x, flag):
        cnt = 0
        try:
            wiki = textblob.TextBlob(x)
            for tup in wiki.tags:
                ppo = list(tup)[1]
                if ppo in pos_family[flag]:
                    cnt += 1
        except:
            pass
        return cnt

    trainDF['noun_count'] = trainDF['text'].apply(lambda x: check_pos_tag(x, 'noun'))
    trainDF['verb_count'] = trainDF['text'].apply(lambda x: check_pos_tag(x, 'verb'))
    trainDF['adj_count'] = trainDF['text'].apply(lambda x: check_pos_tag(x, 'adj'))
    trainDF['adv_count'] = trainDF['text'].apply(lambda x: check_pos_tag(x, 'adv'))
    trainDF['pron_count'] = trainDF['text'].apply(lambda x: check_pos_tag(x, 'pron'))


def train_model(classifier, feature_vector_train, label, feature_vector_valid, is_neural_net=False):
    # fit the training dataset on the classifier
    classifier.fit(feature_vector_train, label)
    
    # predict the labels on validation dataset
    predictions = classifier.predict(feature_vector_valid)
    
    if is_neural_net:
        predictions = predictions.argmax(axis=-1)
    
    return metrics.accuracy_score(predictions, valid_y)


def test_model():
    accuracy = 0
    # Naive Bayes on Count Vectors
    for i in range(0,10):
        accuracy += train_model(naive_bayes.MultinomialNB(), xtrain_count, train_y, xvalid_count)
    print("NB, Count Vectors: ", accuracy/10)

    accuracy = 0
    # Naive Bayes on Word Level TF IDF Vectors
    for i in range(0,10):
        accuracy += train_model(naive_bayes.MultinomialNB(), xtrain_tfidf, train_y, xvalid_tfidf)
    print("NB, WordLevel TF-IDF: ", accuracy/10)

    # Linear Classifier on Count Vectors
    accuracy = 0
    for i in range(0,10):
        accuracy += train_model(linear_model.LogisticRegression(), xtrain_count, train_y, xvalid_count)
    print("LR, Count Vectors: ", accuracy/10)

    # Linear Classifier on Word Level TF IDF Vectors
    accuracy = 0
    for i in range(0,10):
        accuracy += train_model(linear_model.LogisticRegression(), xtrain_tfidf, train_y, xvalid_tfidf)
    print("LR, WordLevel TF-IDF: ", accuracy/10)

# load the dataset
# directory of jsons to be parsed
if samples:
    directory = "/Volumes/KINGSTON/txtlab/out/added_as_text/samples/"
else:
    directory = "/Volumes/KINGSTON/txtlab/out/added_as_text/"

folder_list = [f for f in os.listdir(directory) if not f.startswith('.')]
file_list = []
for folder in folder_list:
    file_list+=([folder+"/"+f for f in os.listdir(directory+folder) if not f.startswith('.')])

print(train_type)
if train_type == 'medium':
    trainDF = medium_as_label(file_list)
else:
    if train_type == 'year':
        print("The base is " + str(base))
    trainDF = meta_as_label(file_list, train_type)

# split the dataset into training and validation datasets 
train_x, valid_x, train_y, valid_y = model_selection.train_test_split(trainDF['text'], trainDF['label'])

# label encode the target variable 
encoder = preprocessing.LabelEncoder()
train_y = encoder.fit_transform(train_y)
valid_y = encoder.fit_transform(valid_y)

# create a count vectorizer object 
count_vect = CountVectorizer(analyzer='word', token_pattern=r'\w{1,}')
count_vect.fit(trainDF['text'])

# transform the training and validation data using count vectorizer object
xtrain_count =  count_vect.transform(train_x)
xvalid_count =  count_vect.transform(valid_x)

# word level tf-idf
tfidf_vect = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', max_features=5000)
tfidf_vect.fit(trainDF['text'])
xtrain_tfidf =  tfidf_vect.transform(train_x)
xvalid_tfidf =  tfidf_vect.transform(valid_x)


test_model()
