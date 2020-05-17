import requests
import bs4
from bs4 import BeautifulSoup
import json
import numpy
from scipy import stats
import matplotlib.pyplot as plt


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


def plotDiagramm(label, data):
    plt.bar(label["category"], data)
    plt.title(label["title"])
    plt.xlabel(label["xlabel"])
    plt.ylabel(label["ylabel"])
    plt.show()


def calculateMeanAndStd(no_lockdown, lockdown):
    return {
        "no_lockdown": {"mean": numpy.mean(no_lockdown), "std": numpy.std(no_lockdown)},
        "lockdown": {"mean": numpy.mean(lockdown), "std": numpy.std(lockdown)},
    }


def welch_ttest(x, y):
    ## Welch-Satterthwaite Degrees of Freedom ##
    dof = (x.var() / x.size + y.var() / y.size) ** 2 / (
        (x.var() / x.size) ** 2 / (x.size - 1) + (y.var() / y.size) ** 2 / (y.size - 1)
    )

    t, p = stats.ttest_ind(x, y, equal_var=False)
    return dof, t, p


states = [
    "deutschland",
    "baden-württemberg",
    "bayern",
    "berlin",
    "brandenburg",
    "bremen",
    "hamburg",
    "hessen",
    "mecklenburg-vorpommern",
    "niedersachsen",
    "nordrhein-westfalen",
    "rheinland-pfalz",
    "saarland",
    "sachsen",
    "sachsen-anhalt",
    "schleswig-holstein",
    "thüringen",
]
# for current_state in states:
current_state = "bremen"
lockdown_date = "2020-03-24"

reproduction_numbers_dataset = extractReproductionNumbers(current_state)

no_lockdown, lockdown = splitSeperationNumbersByDate(
    reproduction_numbers_dataset, lockdown_date
)

mean_and_std = calculateMeanAndStd(no_lockdown, lockdown)
dof, t_val, p_val = welch_ttest(numpy.array(no_lockdown), numpy.array(lockdown))

if p_val > 0.05:
    print(current_state + " :lockdown KEINEN signifikaten einfluss auf r!!")


plotDiagramm(
    {
        "category": ["no_lockdown (< 24.03.20)", "lockdown (>= 24.03.20)"],
        "title": "corona reproduktionszahl vor / während des lockdowns in "
        + current_state,
        "xlabel": "zustandunterscheidungen",
        "ylabel": "reproduktionszahl r",
    },
    [numpy.mean(no_lockdown), numpy.mean(lockdown)],
)