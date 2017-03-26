
from bs4 import BeautifulSoup
import urllib.request
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("url_file", type=str, nargs=1, help="File that holds list of recipe URLs")
args = parser.parse_args()

url_file = open(str(args.url_file[0]))

for url in url_file:
    print(url)


#try:local_filename, headers = urllib.request.urlretrieve(str(args.url[0]))
#except:
 #   print("\n### Unable to open webpage ### \n")
  #  exit(-1)
