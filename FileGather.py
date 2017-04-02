import urllib

from bs4 import BeautifulSoup

filename = "html/test.html"
cuisine = "chinese"
main_url = "http://allrecipes.com/recipes/695/world-cuisine/asian/chinese/?page=1"

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

filenum = 0
for url in url_list:
    urlname = "http://allrecipes.com" + url
    html_filename = "html/" + cuisine +"/" + cuisine + str(filenum) + ".html"

    html_file = open(html_filename, 'w')
    print(urlname)
    
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
