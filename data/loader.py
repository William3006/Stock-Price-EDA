import os
CSV_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "csv_saves")
os.makedirs(CSV_DIR, exist_ok=True)

import matplotlib
import sys
if sys.platform == 'linux':
    try:
        matplotlib.use("module://matplotlib-backend-kitty")
    except Exception:
        pass

import pandas as pd
import yfinance as yf

def load_new(Name_of_stock, Period):
    ticker = yf.Ticker(Name_of_stock)
    data = ticker.history(period=Period)
    return pd.DataFrame(data)

def load_raw(name, i=None, j=None):
    path = os.path.join(CSV_DIR, f"{name}.csv")
    if i is None or j is None:
        return pd.read_csv(path, index_col='Date', parse_dates=True)
    return pd.read_csv(path, skiprows=i, nrows=j, index_col='Date', parse_dates=True)

def save(df, name):
    path = os.path.join(CSV_DIR, f"{name}.csv")
    df.to_csv(path, index=True)
    print(f"Saved Successfully to {path}!")
