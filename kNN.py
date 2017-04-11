import os
import editdistance as edist

def GetFile(fileName, path):
    _file = open(path + fileName, 'r')
    recipeList = _file.read().split('\n')
    _file.close()

    return recipeList

def GetNeighbors(recipe, trainRecipes):
    
    distList = []

    for line in trainRecipes:
        editDist = int(edist.eval(recipe, line))
        distList.append(editDist)

    return distList


def kNN(fileName, trainFiles, trainPath, testPath):
    testRecipes = GetFile(fileName, testPath)

    for recipe in testRecipes:
        recipeMap = {}

        for _file in trainFiles:
            print(_file)
            cuisine = _file.strip(".txt")
            trainRecipes = GetFile(_file, trainPath)

            distList = GetNeighbors(recipe, trainRecipes)

            # Could be faster
            if cuisine in recipeMap.keys():
                recipeMap[cuisine] += distList
            else:
                recipeMap[cuisine] = distList

    print(recipeMap)
    exit(-1)


def main():
    trainPath = "Data/train/"
    testPath = "Data/test/"
    
    trainFiles = os.listdir(trainPath)
    testFiles = os.listdir(testPath)

    for fileName in testFiles:
        kNN(fileName, trainFiles, trainPath, testPath)
    

main()
