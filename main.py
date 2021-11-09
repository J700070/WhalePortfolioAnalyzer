import pandas as pd
from getWhalePortfolio import getData
from analyzePortfolio import *
import numpy as np


# List of funds to analyze
funds_tickers = ["MKL", "GFT", "psc", "LMM", "oaklx", "ic", "DJCO", "TGM",
                 "AM", "aq", "oc", "HC", "SAM", "PI", "DA", "BAUPOST", "FS", "GR", "BRK"]
#funds_tickers = ["PI", "SAM", "DJCO"]
funds_names = []
funds_period = []
funds_portfolio_date = []
funds_num_of_positions = []
funds_top_10_holdings_weight = []
funds_value = []
funds_average_return_open_pos = []

# List of all stocks in the portfolios (Actually a set because we dont want more than 1 instance per stock ticker)
stock_set = set([])

# Fund data from getWhalePortfolio function
funds_data = []

# Data extraction
for fund_ticker in funds_tickers:
    print("Processing 1: " + fund_ticker)
    fund_data = getData(fund_ticker)
    funds_data.append([fund_ticker, fund_data[-1]])

    # Fund positions
    df = fund_data[-1]
    df["Ticker"].apply(lambda x: stock_set.add(x))

    funds_names.append(fund_data[0])
    funds_period.append(fund_data[1])
    funds_portfolio_date.append(fund_data[2])
    funds_num_of_positions.append(df["Stock"].count())
    funds_top_10_holdings_weight.append(
        df["Portfolio (%)"].iloc[0:10].sum())
    funds_value.append(df["Value"].sum())
    funds_average_return_open_pos.append(
        df["Reported Price Change (%)"].mean())


# Matrix of Stocks (columns) and Funds (Rows)
stocks_funds_matrix = np.zeros((len(funds_tickers), len(stock_set)), float)
stocks_funds_df = pd.DataFrame(stocks_funds_matrix)
stocks_funds_df.columns = stock_set
stocks_funds_df.index = funds_tickers

# We register stock weights in the matrix
for fund_ticker, df in funds_data:
    print("Processing 2: " + fund_ticker)
    stocks_funds_df.at[fund_ticker] = df["Portfolio (%)"]

# Funds without a position will have a NaN in place, we substitute those for 0's
stocks_funds_df = stocks_funds_df.fillna(0)

countOpenPositions(stocks_funds_df)
print("All funds processed.")


funds_df = pd.DataFrame(data={
    "Ticker": funds_tickers,
    "Name": funds_names,
    "Period": funds_period,
    "Portfiolio Date": funds_portfolio_date,
    "Number of Positions": funds_num_of_positions,
    "Top 10 Holdings Weight (%)": funds_top_10_holdings_weight,
    "Value ($)": funds_value,
    "Average Return in Open Positions (%)": funds_average_return_open_pos
})

# Print Results
print("\n")
print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
print("\n")
# Funds info
print(funds_df)
print("\n\n\n")
# Funds / Stock Matrix
print(stocks_funds_df)
print("\n\n\n")
# Number of funds that own each stock
print(countOpenPositions(stocks_funds_df))
print("\n\n\n")
