import os
import nltk

def GetFile(fileName, path):
    _file = open(path + fileName, 'r')
    recipeList = _file.read().split('\n')
    recipeList.pop()
    _file.close()

    return recipeList

def WriteToFile(filename, path, wordList):
    _file = open(path + filename, 'w')
    for word in wordList:
        _file.write(word + "\n")

    _file.close()
    pass

def PoS(wordMap, cuisineList, verbList):
    posMap = {}
    verbMap = {}

    for cuisine in cuisineList:
        print(cuisine)
        posMap[cuisine] = []
        verbMap[cuisine] = []
        for recipe in wordMap[cuisine]:
            text = nltk.word_tokenize(recipe)
            tagged = nltk.pos_tag(text)
            
            posStr = ""
            verbStr = ""
            for pair in tagged:
                if pair[0] == "|":
                    continue

                posStr += (pair[1] + " ")
                
                if pair[1] in verbList:
                    verbStr += (pair[0] + " ")

            posMap[cuisine].append(posStr)
            verbMap[cuisine].append(verbStr)
                
    return [verbMap, posMap]

def GetGivenWords(wordList, wordMap, cuisineList):
    wordOutMap = {}
    for cuisine in cuisineList:
        wordOutMap[cuisine] = []
        for recipe in wordMap[cuisine]:
            recipeStr = ""
            recipe = recipe.split(" ")
            for word in recipe:
                if word.lower() in wordList:
                    recipeStr += (word.lower() + " ")

            wordOutMap[cuisine].append(recipeStr)

    return wordOutMap


def main():

    fileList = ["chinese.txt", "caribbean.txt", "french.txt", "italian.txt", "mexican.txt"]
    verbList = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
    nounList = ["NN", "NNS", "NNP", "NNPS"]
    verbNounList = verbList + nounList
    wordFile = open("Data/features/cookverbs/cookingverbs.csv")
    wordList = wordFile.read().lower().split("\n")
    wordFile.close()

    filePath = "Data/"
    posPath = "Data/features/pos/"
    ingPath = "Data/features/ingredients/"
    verbPath = "Data/features/verbs/"
    nounPath = "Data/features/nouns/"
    verbNounPath = "Data/features/verbnouns/"
    cookingPath = "Data/features/cookverbs/"

    ingMap = {}
    verbMap = {}
    cuisineList = []

    for _file in fileList:
        cuisine = _file.strip(".txt")
        cuisineList.append(cuisine)
        recipeList = GetFile(_file, filePath)
        verbMap[cuisine] = recipeList

        for recipe in recipeList:
            splitRecipe = recipe.split("|")

            if len(splitRecipe) > 2:
                print("ERROR: TOO many | in map")
                exit(-1)

            if cuisine in ingMap.keys():
                ingMap[cuisine].append(splitRecipe[0])
            else:
                ingMap[cuisine] = [splitRecipe[0]]

    pos = PoS(verbMap, cuisineList, verbList)
    noun = PoS(verbMap, cuisineList, nounList)[0]
    verbnoun = PoS(verbMap, cuisineList, verbNounList)[0]
    cookVerbs = GetGivenWords(wordList, verbMap, cuisineList)
    verb = pos[0]
    posMap = pos[1]

    for cuisine in cuisineList:
        filename = cuisine + ".txt"
        
        WriteToFile(filename, verbPath, verb[cuisine])
        WriteToFile(filename, ingPath, ingMap[cuisine])
        WriteToFile(filename, posPath, posMap[cuisine])
        WriteToFile(filename, nounPath, noun[cuisine])
        WriteToFile(filename, verbNounPath, verbnoun[cuisine])
        WriteToFile(filename, cookingPath, cookVerbs[cuisine])

main()
