import os
from bs4 import BeautifulSoup
import urllib.request
import argparse


def ParseRecipe(html):

    soup = BeautifulSoup(html, 'html.parser')

    ingredient_list = []
    instruction_list = []

    for ingredient in soup.find_all("span", class_="recipe-ingred_txt added"):
        ingredient_list.append(ingredient.next)

    for instruction in soup.find_all("span", class_="recipe-directions__list--item"):
        instruction = str(instruction.text).replace('\n', '')

        if instruction != "":
            instruction_list.append(instruction)

    return [ingredient_list, instruction_list]


def FormatData(data):
    punct = ['.', '?', '!', ',', ';', ':']

    recipe_data = ""

    for item in data:
        words = item.split()

        for word in words:
            if word[-1] in punct and len(word) > 1:
                if word[-2] != " ":
                    end = word[-1]
                    word = word[:-1] + " " + end
            
            recipe_data += ( word + " " )

    return recipe_data


def WriteToFile(data_set, fileName):
    cuisineFile = open(fileName, 'w')

    for line in data_set:
        cuisineFile.write(line + "\n")

    cuisineFile.close()
    pass


def main():
    #parser = argparse.ArgumentParser()
    #parser.add_argument("cuisine", type=str, nargs=1, help="Cuisine directory name to turn into data set")
    #args = parser.parse_args()
    cuisine_list = [ "chinese",  "italian", "mexican", "caribbean", \
            "french", "irish", "japanese", "middleeastern", "african", "indian"]
    
    for cuisine in cuisine_list:
        
       # cuisine = str(args.cuisine[0])
        path = "html/" + cuisine + "/"
        file_list = sorted(os.listdir(path))
        fileName = "Data/" + cuisine + ".txt"
        data_set = []

        for html_file in file_list:
            print(html_file)
            temp = open(path + html_file)
            html = temp.read()
            temp.close()

            recipeData = ParseRecipe(html)

            ingredients = FormatData(recipeData[0])
            instructions = FormatData(recipeData[1])
            data_set.append(ingredients + " " + instructions)

        WriteToFile(data_set, fileName)

    return 0

main()
