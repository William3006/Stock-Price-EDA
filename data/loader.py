import matplotlib
import sys
if sys.platform == 'linux':
    matplotlib.use("module://matplotlib-backend-kitty")

import pandas as pd

import yfinance as yf





def load_new(Name_of_stock, Period):
    ticker = yf.Ticker(Name_of_stock)
    data = ticker.history(period=Period)
    return pd.DataFrame(data)


def load_raw(name, i=None, j=None):
    
    if i is None or j is None:
        return pd.read_csv(f"csv_saves/{name}.csv", index_col='Date', parse_dates=True)
    
    return pd.read_csv(f"csv_saves/{name}.csv", skiprows=i, nrows=j, index_col='Date', parse_dates=True)


def save(df, name):
    df.to_csv(f"csv_saves/{name}.csv", index=True)
    print(f"Saved Successfully to csv_saves/{name}.csv!")

