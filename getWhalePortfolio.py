import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np


def getData(holding_ticker):
    # Data Extraction
    # We obtain the HTML from the corresponding fund in Dataroma.

    html = requests.get(
        "https://www.dataroma.com/m/holdings.php?m="+holding_ticker, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0"
        }).content

    # Non-table Data Parsing
    soup = BeautifulSoup(html, "html.parser")

    name = soup.find(id="f_name").text
    # Name sometimes doesn't get properly formatted
    name = name.split("\n")[0]

    other_info = soup.find(id="p2").findAll('span')
    period = other_info[0].text
    portfolio_date = other_info[1].text

    df_list = pd.read_html(html)
    df = df_list[0]

    # Data formatting

    # "History" & "Unnamed: 7" columns are not useful.
    df = df.drop(columns=['History', 'Unnamed: 7'])

    # "% ofPortfolio" is not a good name for a column.
    df = df.rename(columns={"% ofPortfolio": "Percentage of Portfolio"})

    # Dollar sign isn't required in "Value" column, it must be a number.
    df["Value"] = df["Value"].apply(parseValueColumnToNumber)
    # We convert the column type to numerical
    df["Value"] = pd.to_numeric(df["Value"])

    # "+/-ReportedPrice" is not a good name for a column.
    df = df.rename(columns={"+/-ReportedPrice": "Change in Reported Price"})

    df["Change in Reported Price"] = df["Change in Reported Price"].replace(
        np.nan, "0")

    # Percentage sign isn't required in "Value" column & must be a number.
    df["Change in Reported Price"] = df["Change in Reported Price"].apply(
        parseReturnsColumnToNumber)
    df["Change in Reported Price"] = pd.to_numeric(
        df["Change in Reported Price"])

    return [name, period, portfolio_date, df]


# We delete the dollar sign and the commas
def parseValueColumnToNumber(string):
    res = ""
    for char in string:
        if(char.isdigit()):
            res += char
    return res


# We delete the dollar sign and the commas
def parseReturnsColumnToNumber(string):
    return string.replace("%", "")
