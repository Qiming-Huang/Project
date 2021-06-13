import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# read the html
response = requests.get("https://learn.lboro.ac.uk/archive/olmp/olmp_resources/pages/wbooks_fulllist.html")
html = response.text

soup = BeautifulSoup(html,'lxml')

url_list = []

# re and get the .pdf urls
for t in soup.find_all('a'):
    if t.get('href')[0] != '.' and t.get('href')[-1] == 'f':
        url_list.append(t.get('href'))

main_path = 'https://learn.lboro.ac.uk/archive/olmp/olmp_resources/pages/'

# download filds and stores
for i in tqdm(range(len(url_list))):
    down_res = requests.get(main_path + url_list[i])
    with open("./pdf/" + str(i) + ".pdf","wb") as code:
        code.write(down_res.content)

