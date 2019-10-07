# sklearn packages
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import model_selection, linear_model, metrics

import pandas as pd
import numpy as np
import os
from math import floor
import statistics
import enchant

sample = False
medium = 'tv'
cls_value = 'genre'


print("Test: " + cls_value + "\nMedium: " + medium)
print("Sample: " + str(sample))
if sample:
    trainDF=pd.read_pickle("/Volumes/NATHAN/out/classification_meta/complete_features_sample.pkl")
else:
    trainDF = pd.read_pickle('/Volumes/NATHAN/out/classification_meta/complete_features.pkl')

def to_lower(s):
    try:
        s = str(s).lower()
    except:
        s = None
    return s


def in_dictionary(string):
    d = enchant.Dict("en_US")
    words = string.split(' ')
    new_words = []
    for word in words:
        try:
            in_dict = d.check(word)
        except:
            continue
        if in_dict:
            new_words.append(word)
    string = ' '.join(str(x) for x in new_words)
    return string


trainDF['GENRE'] = trainDF['GENRE'].apply(to_lower)

trainDF = trainDF[trainDF['TEXT'] != None]
trainDF = trainDF[pd.notnull(trainDF.TEXT)]

if cls_value == 'genre':
    trainDF = trainDF[pd.notnull(trainDF.GENRE)]
    trainDF = trainDF[(trainDF['MEDIUM'] == medium)]
    drama = trainDF[(trainDF['GENRE'] == 'drama')]
    comedy = trainDF[(trainDF['GENRE'] == 'comedy')]
    trainDF = pd.concat([drama,comedy])


trainDF['TEXT'] = trainDF['TEXT'].apply(in_dictionary)

if medium == 'all':
    trainDF = trainDF[trainDF['MEDIUM'] != 'novels']


median = trainDF['YEAR'].median()
def check_date(year):
    if year < median:
        return 0
    return 1

def check_genre(genre):
    if genre.lower() == 'comedy':
        return 0
    return 1

trainDF['YEAR'] = trainDF['YEAR'].apply(check_date)
trainDF['GENRE'] = trainDF['GENRE'].apply(check_genre)

print(trainDF)

print("There are " + str(len(trainDF)) + " pages in the current set.")

trainDF = trainDF.reset_index()

vectorizer = CountVectorizer(min_df=3, encoding='utf8')
dtm = vectorizer.fit_transform(trainDF['TEXT'])
vocab = vectorizer.get_feature_names()
matrix = dtm.toarray()

DTM = pd.DataFrame(matrix, columns=vocab)

all_meta = trainDF[['MEDIUM','GENRE','YEAR','YEAR_25', "YEAR_50"]]

final_df = pd.concat([all_meta, DTM], axis=1)

def linear_reg(X,Y):
    # Fit the model, only on training set (no test set)
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, Y, test_size=0.3, random_state=0)

    # Specify regularization penalties
    model2 = linear_model.LogisticRegression(penalty='l1', C=1) # Remember l1 is lasso
    model2.fit(X_train, y_train)

    # predict class labels for the test set
    predicted = model2.predict(X_test)

    # Now, evaluate model with cross-validation
    scores=model_selection.cross_val_score(linear_model.LogisticRegression(penalty='l1', C=1), X, Y, scoring='f1_weighted', cv=30)
    print("Mean: " + str(scores.mean()))
    print("Stdev: " + str(statistics.stdev(scores)))

    # Compute most informative features for binary case
    clf = linear_model.LogisticRegression(penalty='l1', C=0.1)
    clf.fit(X_train, y_train)

    feature_names = final_df.columns[5:].values     

    top20 = np.argsort(np.exp(clf.coef_))[0][-20:]
    print("Top 20 features associated with second class\n")
    # for el,le in zip(feature_names[top20], np.exp(clf.coef_)[0][top20]):
    #     if le > 1:
    #         print(el + " (" + str("%.3f"%le) + ")", end=", ")

    print(list(reversed(feature_names[top20])))
    print(list(reversed(np.exp(clf.coef_)[0][top20])))


    print("\n")
    print("Top 20 features associated with first class\n")
    bottom20 = np.argsort(np.exp(clf.coef_))[0][:20]
    try:
        for el,le in (feature_names[bottom20][:15], np.exp(clf.coef_)[0][bottom20][:15]):
            if le < 1:
                print(el + " (" + str("%.3f"%le) + ")", end=", ")
    except:
        next
    print('\n')
    try:
        print(feature_names[bottom20])
        print(np.exp(clf.coef_)[0][bottom20])
    except:
        next
    print('\n')


X = final_df.iloc[:, 3:].values    # corresponds to where feature columns begin
if cls_value == 'medium':
    Y = final_df.MEDIUM.values # corresponds to where class values are located
elif cls_value == 'genre':
    Y = final_df.GENRE.values
elif cls_value == 'yr_50':
    Y = final_df.YEAR_50.values
elif cls_value == 'yr_25':
    Y = final_df.YEAR_25.values
elif cls_value == 'yr':
    Y = final_df.YEAR.values

linear_reg(X,Y)
