# Classifier.py
#
# Author: Steven Jorgensen
# Date: 04/22/17
# 
# An implementation of 3 different text classifiers.

import os
import editdistance as edist
import heapq as hq
import argparse
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline



def GetFile(fileName, path):
    _file = open(path + fileName, 'r')
    recipeList = _file.read().split('\n')
    recipeList.pop()
    _file.close()

    return recipeList

### KNN functions ##############################################################

def GuessCuisine(recipeMap, k):
    k_list = []
    for cuisine in recipeMap:
        for i in range(k):
            k_list.append((hq.heappop(recipeMap[cuisine]), cuisine))

    guessList = sorted(k_list)
    #print(guessList)
    guessTotal = {}

    for i in range(k):
        if guessList[i][1] in guessTotal.keys():
            guessTotal[guessList[i][1]] += 1
        else:
            guessTotal[guessList[i][1]] = 1
            #print(guessList[i][1])
    
    max_total = 0
    max_cuisine = ""
    #print()
    #print(guessTotal)
    for cuisine in guessTotal.keys():
        if max_total < guessTotal[cuisine]:
            max_total = guessTotal[cuisine]
            max_cuisine = cuisine

    return max_cuisine


def GetNeighbors(trainCuisine, testRecipe, trainMap):
    distList = []
    for trainRecipe in trainMap[trainCuisine]:
        editDist = int(edist.eval(testRecipe, trainRecipe))
        hq.heappush(distList, editDist)
    
    return distList


def kNN(testMap, trainMap, k):
    total = 0
    correct = 0
    for testCuisine in testMap.keys():
        #print(testCuisine)
        gc = 0
        gt = 0
        #if testCuisine != "african":
            #continue
        for testRecipe in testMap[testCuisine]:
            recipeMap = {}
            for trainCuisine in trainMap.keys():
                #print(trainCuisine)
                recipeMap[trainCuisine] = GetNeighbors(trainCuisine, testRecipe, trainMap)
            
            guess = GuessCuisine(recipeMap, k)
            #print "Guess:", guess
            if guess == testCuisine:
                correct += 1
                gc += 1
            total += 1
            gt += 1
        print (testCuisine, gc / float(gt))
        
    print ("FINAL:", correct / float(total))

    pass


### SVM Functions ##############################################################


def SVM(trainMap, testMap, cuisineList):

    #text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB()),])
    text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', SGDClassifier(loss='log', penalty='l2', alpha=1e-3, n_iter=1000, random_state=42)),])

    text_clf = text_clf.fit(trainMap, cuisineList)
    total_all = 0
    correct_all = 0
    for cuisineName in cuisineList:
        
        test = testMap[cuisineName]
        predict = text_clf.predict(test)
        #print(predict)
        correct = 0
        total = 0
        for item in predict:
            total += 1
            total_all += 1
            if item == cuisineName:
                correct += 1
                correct_all += 1
        
        print(cuisineName, correct / float(total))

    print("FINAL:", correct_all / float(total_all)) 
    
    pass


### NB Functions ###############################################################


def NB(trainMap, testMap, cuisineList):

    text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB()),])
    #text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', SGDClassifier(loss='log', penalty='l2', alpha=1e-3, n_iter=1000, random_state=42)),])

    text_clf = text_clf.fit(trainMap, cuisineList)
    total_all = 0
    correct_all = 0
    for cuisineName in cuisineList:
        
        test = testMap[cuisineName]
        predict = text_clf.predict(test)
        #print(predict)
        correct = 0
        total = 0
        for item in predict:
            total += 1
            total_all += 1
            if item == cuisineName:
                correct += 1
                correct_all += 1
        
        print(cuisineName, correct / float(total))

    print("FINAL:", correct_all / float(total_all)) 
    
    pass



#----- Main --------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("classifier", type=str, help="Type of classifier to use. [NB, SVM, KNN]")
    parser.add_argument("k", type=int, action='store', nargs='?',default=0, help="Number of nearest neighbors to use.")
    args = parser.parse_args()
    
    k = args.k
    classifier = args.classifier
    trainPath = "Data/train/"
    testPath = "Data/test/"
    trainFileList = os.listdir(trainPath)
    testFileList = os.listdir(testPath)

    testMap = {}
    trainMap = {}
    knnTrainMap = {}
    cuisineList = []
    format_train = []

    for _file in testFileList:
        cuisine = _file.strip("test-").strip(".txt")
        recipeList = GetFile(_file, testPath)
        testMap[cuisine] = recipeList

    for _file in trainFileList:
        cuisine = _file.strip(".txt")
        cuisineList.append(cuisine)
        recipeList = GetFile(_file, trainPath)
        knnTrainMap[cuisine] = recipeList
        trainMap[cuisine] = " ".join(recipeList)

    for cuisineID in cuisineList:
        format_train.append(trainMap[cuisineID])

    if classifier == "NB":

        if k != 0:
            print("This classifier does not require a K. Exiting.")
            exit(-1)

        NB(format_train, testMap, cuisineList)

    elif classifier == "SVM":

        if k != 0:
            print("This classifier does not require a K. Exiting.")
            exit(-1)

        SVM(format_train, testMap, cuisineList)

    elif classifier == "KNN":

        if k == 0:
            print("No specified K. Please enter a K value.")
            exit(-1)

        kNN(testMap, knnTrainMap, k)

    else:
        print("Invalid classifier. The options are NB, KNN, or SVM.")
        exit(-1)
    
    
    pass

main()
