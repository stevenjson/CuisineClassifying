
from bs4 import BeautifulSoup
import urllib.request
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("url_file", type=str, nargs=1, help="File that holds list of recipe URLs")
args = parser.parse_args()

url_file = open(str(args.url_file[0]))

data_set = []

for url in url_file:
    url = url.strip()
    print(url)


    try:local_filename, headers = urllib.request.urlretrieve(url)
    except:
        print("\n### Unable to open webpage " + url + " ### \n")
        exit(-1)

    html = open(local_filename).read()
    soup = BeautifulSoup(html, 'html.parser')

    ingredient_list = []
    instruction_list = []

    for ingredient in soup.find_all("span", class_="recipe-ingred_txt added"):
        ingredient_list.append(ingredient.next)

    for instruction in soup.find_all("span", class_="recipe-directions__list--item"):
        instruction = str(instruction.text).replace('\n', '')

        if instruction != "":
            instruction_list.append(instruction)


    punct = ['.', '?', '!', ',', ';', ':']

    recipe_data = ""

    for ingredient in ingredient_list:
        words = ingredient.split()

        for word in words:
            if word[-1] in punct:
                if word[-2] != " ":
                    end = word[-1]
                    word = word[:-1] + " " + end
            
            recipe_data += ( word + " " )

    print(recipe_data)
