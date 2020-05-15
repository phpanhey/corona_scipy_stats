import requests
import bs4
from bs4 import BeautifulSoup
import json


def extractReproductionNumbers(state):
    url = "https://stochastik-tu-ilmenau.github.io/COVID-19/germany"
    re = requests.get(url)
    soup = BeautifulSoup(re.text, "html.parser")
    data = json.loads(
        soup.find("div", {"id": state})
        .find("script", type="application/json")
        .contents[0]
    )
    reproduction_numbers = data["x"]["data"][0]["y"]
    date_of_reproduction_numbers = data["x"]["data"][0]["x"]

    return {
        "dates": date_of_reproduction_numbers,
        "reproduction_numbers": reproduction_numbers,
    }


reproduction_numbers = extractReproductionNumbers("bayern")
print(reproduction_numbers)
# print(json.dumps(infected_data, indent=4))
