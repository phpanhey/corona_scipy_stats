import requests
import bs4
from bs4 import BeautifulSoup
import json
import statistics


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

    reproduction_numbers = getRidOfNone(reproduction_numbers)
    date_of_reproduction_numbers = getRidOfNone(date_of_reproduction_numbers)

    return {
        "dates": date_of_reproduction_numbers,
        "numbers": reproduction_numbers,
    }


def getRidOfNone(array):
    return [x for x in array if x is not None]


def splitSeperationNumbersByDate(reproduction_numbers_dataset, date_str):
    entry_index = reproduction_numbers_dataset["dates"].index(date_str)
    no_lockdown = reproduction_numbers_dataset["numbers"][:entry_index]
    lockdown = [
        x for x in reproduction_numbers_dataset["numbers"] if x not in no_lockdown
    ]
    return no_lockdown, lockdown


state = "bremen"
lockdown_date = "2020-03-24"
reproduction_numbers_dataset = extractReproductionNumbers(state)
no_lockdown, lockdown = splitSeperationNumbersByDate(
    reproduction_numbers_dataset, lockdown_date
)


print("mittelwert r no_lockdown in " + state + ": " + str(statistics.mean(no_lockdown)))
print('####')
print("mittelwert r lockdown in " + state + ": " + str(statistics.mean(lockdown)))
