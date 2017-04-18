import os
import editdistance as edist
import heapq as hq
import argparse

def GetFile(fileName, path):
    _file = open(path + fileName, 'r')
    recipeList = _file.read().split('\n')
    recipeList.pop()
    _file.close()

    return recipeList

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
        print testCuisine, gc / float(gt)
        
    print "FINAL:", correct / float(total)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("k", type=int, nargs=1, help="Number of nearest neighbors to use.")
    args = parser.parse_args()
    
    k = int(args.k[0])
    trainPath = "Data/train/"
    testPath = "Data/test/"
    
    trainFileList = os.listdir(trainPath)
    testFileList = os.listdir(testPath)
    
    testMap = {}
    trainMap = {}
    
    for _file in testFileList:
        cuisine = _file.strip("test-").strip(".txt")
        recipeList = GetFile(_file, testPath)
        testMap[cuisine] = recipeList

    for _file in trainFileList:
        cuisine = _file.strip(".txt")
        recipeList = GetFile(_file, trainPath)
        trainMap[cuisine] = recipeList
    
    kNN(testMap, trainMap, k)

main()
