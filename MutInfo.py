import math
import argparse

def GetFile(fileName, path):
    _file = open(path + fileName, 'r')
    recipeList = _file.read().split('\n')
    recipeList.pop()
    _file.close()

    return recipeList

def Count(recipeMap, cuisineList, recipeList):
    mutMap = {}

    for word in recipeList:
        for i in range(len(cuisineList)):
            for recipe in recipeMap[cuisineList[i]]:
                recipe = recipe.split(" ")

                if word in recipe:
                    if word in mutMap.keys():
                        mutMap[word][i] += 1
                    else:
                        mutMap[word] = [0]*len(cuisineList)
                        mutMap[word][i] += 1

    return mutMap


def MutInfo(word, countMap, foldSize, totalSize, recipeList, cuisineList):
    probWord = 0
    probClass = foldSize / float(totalSize)
    probWordClass = 0
    mutInfo = 0
    wordTotal = 0

    for item in countMap[word]:
        wordTotal += item

    probWord = wordTotal / float(totalSize)

    for count in countMap[word]:
        probWordClass = count / float(totalSize)

        pointMut = 0.0

        if probWordClass != 0:
            pointMut = (math.log(probWordClass, 2)) + (math.log(probWord * probClass, 2) * -1)


        mutInfo += (probWordClass * pointMut)

    probWord = (totalSize - wordTotal) / float(totalSize)

    for count in countMap[word]:
        probWordClass = (foldSize - count) / float(totalSize)

        pointMut = 0.0

        if probWordClass != 0:
            pointMut = (math.log(probWordClass, 2)) + (math.log(probWord * probClass, 2) * -1)


        mutInfo += (probWordClass * pointMut)

    return mutInfo

def PrintInfo(probMap, countMap, cuisineList, cuisine, n):
    print()

    if cuisine == "all":
        for word in sorted(probMap, key=probMap.get, reverse=True)[:n]:
            maxId = 0
            maxCount = 0
            for i in range(len(countMap[word])):
                if countMap[word][i] > maxCount:
                    maxId = i
                    maxCount = countMap[word][i]
            print("{:15s}: {:.5f}   {:10s}".format(word, probMap[word], cuisineList[maxId]))
            print()
            #print("Counts: {}".format(countMap[word]))
            #print(cuisineList)
    elif cuisine in cuisineList:
        cuisineCount = 0
        for word in sorted(probMap, key=probMap.get, reverse=True):
            if cuisineCount > n:
                break
            
            maxId = 0
            maxCount = 0
            for i in range(len(countMap[word])):
                if countMap[word][i] > maxCount:
                    maxId = i
                    maxCount = countMap[word][i]

            if cuisine == cuisineList[maxId]:
                print("{:15s}: {:.5f}   {:10s}".format(word, probMap[word], cuisineList[maxId]))
                print()
                cuisineCount += 1

    pass



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("feature", type=str, help="Type of feature to use. ")
    parser.add_argument("topN", type=int, help="Top N words to display")
    parser.add_argument("cuisine", type=str, help="Cuisine of interest [all for all cuisines]")
    args = parser.parse_args()

    fileList = ["chinese.txt", "caribbean.txt", "french.txt", "italian.txt", "mexican.txt"]

    feature = args.feature
    cuisineInfo = args.cuisine
    
    if feature != "none":
        filePath = "Data/features/" + feature + "/"
    else:
        filePath = "Data/"

    n = args.topN
    foldSize = 180
    totalSize = 900

    cuisineList = []
    recipeMap = {}
    probMap = {}

    for _file in fileList:
        cuisine = _file.strip(".txt")
        cuisineList.append(cuisine)
        recipeList = GetFile(_file, filePath)
        recipeMap[cuisine] = recipeList

    recipeStr = ""
    for cuisine in cuisineList:
        for recipe in recipeMap[cuisine]:
            recipeStr += (recipe + " ")

    recipeList = set(recipeStr.split(" "))

    countMap = Count(recipeMap, cuisineList, recipeList)
    
    for word in recipeList:
        if word == "" or  word == " ":
            continue
        probMap[word] = MutInfo(word, countMap, foldSize, totalSize, recipeList, cuisineList)
        

    PrintInfo(probMap, countMap, cuisineList, cuisineInfo, n)

    pass

main()
