import urllib
import os
import argparse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("url", type=str, nargs=1, help="Main url with list of recipe URLs")
parser.add_argument("cuisine", type=str, nargs=1, help="Type of cuisine on the main url page")
parser.add_argument("pageNum", type=int, nargs=1, help="Page number to pull from")
#parser.add_argument("fileStart", type=int, nargs=1, help="number to start filenames on")
args = parser.parse_args()

cuisine = str(args.cuisine[0]).lower()
page = str(args.pageNum[0])
main_url = str(args.url[0]) + "?page=" + page

try:local_filename, headers = urllib.request.urlretrieve(main_url)
except:
    print("\n### Unable to open webpage " + url + " ### \n")
    exit(-1)

url_file = open(local_filename)
html = url_file.read()
soup = BeautifulSoup(html, 'html.parser')

div = soup.find_all('article', class_='grid-col--fixed-tiles')

url_list = []

for item in div:
    for a in item.find_all('a', href=True):
        if "/recipe" in a['href']:
            if a['href'] not in url_list:
                url_list.append(a['href'])
                
                
url_file.close()

filenum = len(os.listdir("html/" + cuisine))
for url in url_list:
    urlname = "http://allrecipes.com" + url
    html_filename = "html/" + cuisine +"/" + cuisine + str(filenum) + ".html"

    html_file = open(html_filename, 'w')
    print(urlname, filenum)
    
    try:local_filename, headers = urllib.request.urlretrieve(urlname)
    except:
        print("UNABLE TO OPEN " + urlname)
        exit(-1)

    file_ = open(local_filename)
    data = file_.read()
    

    html_file.write(data)
    html_file.close()
    file_.close()
    
    filenum += 1
    

print("Done")
