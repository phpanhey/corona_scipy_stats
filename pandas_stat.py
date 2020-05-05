import requests
import bs4
from bs4 import BeautifulSoup
import re
import json


def getInfectionRelatedUrls(parent_url):
    base_url = 'https://www.senatspressestelle.bremen.de/'
    res = []
    re = requests.get(parent_url)
    soup = BeautifulSoup(re.text, "html.parser")
    for a in soup.find_all('a', href=True):
        if 'detail.php?gsid=bremen146.c.' in a['href']:
            res.append(base_url + a['href'])
    return res


def extractInfectedWithUrl(url):
    re = requests.get(url)
    soup = BeautifulSoup(re.text, "html.parser")
    td_soup = soup.find('td')
    amount_of_infected = 0
    if td_soup != None:
        amount_of_infected = clearString(td_soup.contents[0])
    article_time = soup.find("span", {"class": "article_time"}).contents[0]
    return {'article_time': article_time, 'amount_of_infected': amount_of_infected}


def clearString(str):
    return re.sub('\(.*?\)', '', str, flags=re.DOTALL).strip()


def extractInfectedWithUrls(urls):
    res = []
    for url in urls:
        res.append(extractInfectedWithUrl(url))
    return res


partent_url = 'https://www.senatspressestelle.bremen.de/list.php?template=20_pmsuche_treffer_l&query=10_pmalle_q&sv%5Bonline_date%5D%5B%5D=%3E--&sv%5Bfulltext%5D=Aktueller%20Stand%20Corona&sv%5Bfulltext2%5D=Aktueller%20Stand%20Corona&sm%5Bfulltext%5D=fulltext_all&sm%5Bfulltext2%5D=fulltext_all&sort=online_date&order=desc&suche=Aktueller%20Stand%20Corona&wie=1&von='
urls = getInfectionRelatedUrls(partent_url)
infected_data = extractInfectedWithUrls(urls)
print(json.dumps(infected_data, indent=4))

