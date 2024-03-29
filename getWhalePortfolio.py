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

    # "History", "52WeekLow", "52WeekHigh" & "Unnamed: 7" columns are not useful.
    df = df.drop(columns=['History', 'Unnamed: 7', "52WeekLow", "52WeekHigh"])

    # Column name corrections.
    df = df.rename(columns={"% ofPortfolio": "Portfolio (%)"})
    df = df.rename(columns={"+/-ReportedPrice": "Reported Price Change (%)"})
    df = df.rename(columns={"ReportedPrice*": "Reported Price"})
    df = df.rename(columns={"RecentActivity": "Recent Activity"})

    # Nan corrections
    df["Reported Price Change (%)"] = df["Reported Price Change (%)"].replace(
        np.nan, "0")

    # Data format & type corrections.
    df["Value"] = df["Value"].apply(parseValueColumnToNumber)
    df["Value"] = pd.to_numeric(df["Value"])

    df["Reported Price Change (%)"] = df["Reported Price Change (%)"].apply(
        parseReturnsColumnToNumber)
    df["Reported Price Change (%)"] = pd.to_numeric(
        df["Reported Price Change (%)"])

    # Ticker and name of the stock are inside the same columns, we are going to slit it into 2 different columns
    df["Ticker"] = df["Stock"].apply(lambda x: x.split(" - ")[0])
    df.index = df["Stock"].apply(lambda x: x.split(" - ")[0])
    df["Stock"] = df["Stock"].apply(lambda x: x.split(" - ")[1])

    # We move "Ticker" column to the front
    col = df.pop("Ticker")
    df.insert(0, col.name, col)

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


def getDataBuys(holding_ticker):
    # Data Extraction
    # We obtain the HTML from the corresponding fund in Dataroma.

    html = requests.get(
        "https://www.dataroma.com/m/m_activity.php?m="+holding_ticker + "&typ=b", headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
            "Accept": "image/avif,image/webp,*/*",
            "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
            "Sec-Fetch-Dest": "image",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-origin",
            "Cache-Control": "max-age=0"
        }).content

    df_list = pd.read_html(html)
    df = df_list[0]
    print(df.head())
    return
