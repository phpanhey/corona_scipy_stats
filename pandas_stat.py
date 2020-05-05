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
    return {article_time : amount_of_infected}


def clearString(str):
    return re.sub('\(.*?\)', '', str, flags=re.DOTALL).strip()


def extractInfectedWithUrls(urls):
    res = {}
    for url in urls:
        res.update(extractInfectedWithUrl(url))
    return res

def addMissingInfections(infected_data):
    infected_data["11.03.2020"] = 0
    infected_data["10.03.2020"] = 0
    infected_data["09.03.2020"] = 0
    infected_data["06.03.2020"] = 0
    infected_data["05.03.2020"] = 0
    infected_data["04.03.2020"] = 0
    infected_data["03.03.2020"] = 0
    infected_data["02.03.2020"] = 0
    infected_data["01.03.2020"] = 0
    infected_data["28.02.2020"] = 0
    return infected_data


# partent_url = 'https://www.senatspressestelle.bremen.de/list.php?template=20_pmsuche_treffer_l&query=10_pmalle_q&sv%5Bonline_date%5D%5B%5D=%3E--&sv%5Bfulltext%5D=Aktueller%20Stand%20Corona&sv%5Bfulltext2%5D=Aktueller%20Stand%20Corona&sm%5Bfulltext%5D=fulltext_all&sm%5Bfulltext2%5D=fulltext_all&sort=online_date&order=desc&suche=Aktueller%20Stand%20Corona&wie=1&von='
# urls = getInfectionRelatedUrls(partent_url)
# infected_data = extractInfectedWithUrls(urls)

infected_data = {"04.05.2020":894,"03.05.2020":893,"02.05.2020":875,"30.04.2020":859,"29.04.2020":827,"28.04.2020":796,"27.04.2020":759,"26.04.2020":754,"25.04.2020":740,"24.04.2020":720,"23.04.2020":708,"22.04.2020":673,"21.04.2020":625,"20.04.2020":607,"19.04.2020":601,"18.04.2020":582,"17.04.2020":564,"16.04.2020":553,"15.04.2020":504,"14.04.2020":497,"13.04.2020":489,"11.04.2020":477,"09.04.2020":451,"08.04.2020":442,"07.04.2020":422,"06.04.2020":395,"05.04.2020":393,"04.04.2020":388,"03.04.2020":354,"02.04.2020":341,"01.04.2020":330,"31.03.2020":315,"30.03.2020":297,"29.03.2020":290,"28.03.2020":278,"27.03.2020":263,"26.03.2020":244,"25.03.2020":212,"24.03.2020":195,"23.03.2020":175,"22.03.2020":173,"21.03.2020":168,"20.03.2020":127,"19.03.2020":119,"18.03.2020":75,"17.03.2020":66,"16.03.2020":57,"15.03.2020":56,"14.03.2020":53,"13.03.2020":48,"12.03.2020":42,"11.03.2020":0,"10.03.2020":0,"09.03.2020":0,"06.03.2020":0,"05.03.2020":0,"04.03.2020":0,"03.03.2020":0,"02.03.2020":0,"01.03.2020":0,"28.02.2020":0}
infected_data = addMissingInfections(infected_data)



print(json.dumps(infected_data, indent=4))

