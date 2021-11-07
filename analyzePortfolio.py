def sortByConcentration(dataframe):
    return dataframe.sort_values(by=["Top 10 Holdings Weight (%)"])


def aux(fund_ticker, stocks_funds_df, x, df):
    stocks_funds_df.at[fund_ticker, x] = df.at[x, "Portfolio (%)"]
    print(stocks_funds_df)
    return
