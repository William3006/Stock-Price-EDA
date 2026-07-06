import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf

"""
For initial collection of data and storage
    meta = yf.Ticker("META")
    data = meta.history(period="10y")
    df = pd.DataFrame(data)

df.to_csv("csv_saves/OHLCV_META_10y.csv", index = False)
"""

# print(data.to_string())
"""
For initial visualisation of data and storage of plots
    plt.plot(data.index, data["Open"], label="Open")
    plt.plot(data.index, data["Close"], label="Close")
    plt.xlabel("Date")
    plt.ylabel("Opening and closing prices")
    os.makedirs("Meta_Plots", exist_ok=True)
    plt.savefig("Meta_Plots/OC(1m)")
"""

df = pd.read_csv("csv_saves/OHLCV_META_10y.csv")


# single variate analysis

df["Net"] = df["Close"] - df["Open"]
df["Profit"] = df["Net"] > 0
num_of_profit_days = df["Profit"].sum()

df.to_csv("csv_saves/NP_META_10y.csv", index=False)
print(df, num_of_profit_days)

# multivariate analysis
