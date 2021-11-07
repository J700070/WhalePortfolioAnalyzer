import pandas as pd
from getWhalePortfolio import getData
from analyzePortfolio import analyzePortfolio
import numpy as np

# List of funds to analyze
funds_tickers = ["MKL", "GFT", "psc", "LMM", "oaklx", "ic", "DJCO", "TGM",
                 "AM", "aq", "oc", "HC", "SAM", "PI", "DA", "BAUPOST", "FS", "GR", "BRK"]
# funds_tickers = ["LMM"]
funds_names = []
funds_period = []
funds_portfolio_date = []
funds_num_of_positions = []
funds_top_10_holdings_weight = []
funds_value = []
funds_average_return_open_pos = []

#

for fund_ticker in funds_tickers:
    print(fund_ticker)
    fund_data = getData(fund_ticker)
    df = fund_data[-1]
    funds_names.append(fund_data[0])
    funds_period.append(fund_data[1])
    funds_portfolio_date.append(fund_data[2])
    funds_num_of_positions.append(df["Stock"].count())
    funds_top_10_holdings_weight.append(
        df["Percentage of Portfolio"].iloc[0:10].sum())
    funds_value.append(df["Value"].sum())
    funds_average_return_open_pos.append(df["Change in Reported Price"].mean())
    analyzePortfolio(df)

funds_df = pd.DataFrame(data={
    "Ticker": funds_tickers,
    "Name": funds_names,
    "Period": funds_period,
    "Portfiolio Date": funds_num_of_positions,
    "Number of Positions": funds_num_of_positions,
    "Top 10 Holdings Weight": funds_top_10_holdings_weight,
    "Value": funds_value,
    "Average Return in Open Positions": funds_average_return_open_pos
})
print(funds_df)
