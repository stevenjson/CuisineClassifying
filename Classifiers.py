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

class Fold():
    def __init__(self):
        self.test = {}
        self.train = {}


def GetFile(fileName, path):
    _file = open(path + fileName, 'r')
    recipeList = _file.read().split('\n')
    recipeList.pop()
    _file.close()

    return recipeList

def MakeFolds(foldNum, foldDiv, RecipeMap, foldList):

    for num in range(foldDiv):
        newFold = Fold()
        foldList.append(newFold)

    for cuisine in RecipeMap.keys():
        currFold = -1
        for i in range(len(RecipeMap[cuisine])):
            if i % foldNum == 0:
                currFold += 1

            for j in range(len(foldList)):
                if j == currFold:
                    if cuisine in foldList[j].test.keys():
                        foldList[j].test[cuisine].append(RecipeMap[cuisine][i])
                    else:
                        foldList[j].test[cuisine] = [RecipeMap[cuisine][i]]
                else:
                    if cuisine in foldList[j].train.keys():
                        foldList[j].train[cuisine].append(RecipeMap[cuisine][i])
                    else:
                        foldList[j].train[cuisine] = [RecipeMap[cuisine][i]]

def PrintStats(stats, cuisineList, foldNum, foldLen, foldDiv):
    total_correct = 0
    #print(foldNum, foldLen, foldDiv)

    for cuisine in cuisineList:
        total_correct += stats[cuisine]
        print(cuisine, ": {:.2f}".format(stats[cuisine] / float(foldLen)))

    total = len(cuisineList) * foldLen

    print("OVERALL: {:.2f}".format(total_correct / float(total)))
    

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


def kNN(testMap, trainMap, k, stats, cuisineList):
    total = 0
    correct = 0
    for testCuisine in cuisineList:
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

        stats[testCuisine] += gc
        print (testCuisine, gc / float(gt))
        
    print ("FINAL:", correct / float(total))

    pass


### SVM Functions ##############################################################


def SVM(trainMap, testMap, cuisineList, stats):

    #text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB()),])
    text_clf = Pipeline([('vect', CountVectorizer(ngram_range=(2, 2))), ('tfidf', TfidfTransformer()), ('clf', SGDClassifier(loss='log', penalty='l2', alpha=1e-3, n_iter=1000, random_state=42)),])

    text_clf = text_clf.fit(trainMap, cuisineList)
    #vect.get_feature_names()
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
        
        stats[cuisineName] += correct
        print(cuisineName, correct / float(total))

    print("FINAL:", correct_all / float(total_all)) 
    
    pass


### NB Functions ###############################################################


def NB(trainMap, testMap, cuisineList, stats):

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
        
        stats[cuisineName] += correct
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
    trainPath = "Data/"
    trainFileList = ["chinese.txt", "caribbean.txt", "french.txt", "italian.txt", "mexican.txt"]

    RecipeMap = {}
    cuisineList = []
    stats = {}

    foldDiv = 6 # Number of folds to use

    #for _file in testFileList:
    #    cuisine = _file.strip("test-").strip(".txt")
    #    recipeList = GetFile(_file, testPath)
    #    testMap[cuisine] = recipeList

    for _file in trainFileList:
        cuisine = _file.strip(".txt")
        cuisineList.append(cuisine)
        recipeList = GetFile(_file, trainPath)
        RecipeMap[cuisine] = recipeList

    foldLen = len(RecipeMap[cuisineList[0]])
    foldNum = foldLen / foldDiv

    foldList = []
    MakeFolds(foldNum, foldDiv, RecipeMap, foldList)

    for cuisine in cuisineList:
        stats[cuisine] = 0

    #print(foldList[0].test)
    #for i in range(6):
        #print(len(foldList[i].test["chinese"]))
        #print(len(foldList[i].train["chinese"]))

    num = 1
    for fold in foldList:
        format_train = []

        print("FOLD", num)


        for cuisineID in cuisineList:
            format_train.append(" ".join(fold.train[cuisineID]))
        
        if classifier == "NB":

            if k != 0:
                print("This classifier does not require a K. Exiting.")
                exit(-1)

            NB(format_train, fold.test, cuisineList, stats)

        elif classifier == "SVM":

            if k != 0:
                print("This classifier does not require a K. Exiting.")
                exit(-1)

            SVM(format_train, fold.test, cuisineList, stats)

        elif classifier == "KNN":

            if k == 0:
                print("No specified K. Please enter a K value.")
                exit(-1)

            kNN(fold.test, fold.train, k, stats, cuisineList)

        else:
            print("Invalid classifier. The options are NB, KNN, or SVM.")
            exit(-1)

        print()
        num +=1
    
    PrintStats(stats, cuisineList, foldNum, foldLen, foldDiv)
    
    pass

main()
