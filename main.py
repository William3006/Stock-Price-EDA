import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf


def load_new(Name_of_stock, Period):
    ticker = yf.Ticker(name)
    data = ticker.history(period=period)
    return pd.DataFrame(data)

    
def load_raw(name, i=None, j=None):
    if(i==None or j==None):
        return pd.read_csv(f'csv_saves/{name}.csv')
    
    return pd.read_csv(f'csv_saves/{name}.csv', skiprows=i, nrows=j)


def save(df, name):
    df.to_csv(f'csv_saves/{name}', index=False)
    print(f'Saved Successfully to csv_saves/{name}!')
    

def add_net_profit(raw_data):
    raw_data["Net"] = raw_data["Close"] - raw_data["Open"]
    raw_data["Profit"] = raw_data["Net"] > 0
    return raw_data


def add_rolling(mod1, time_span):
    mod1['Rolling'] = mod1['Close'].rolling(window=time_span).mean()
    return mod1


#add volatility
if __name__ == "__main__":

    #testing load function
    mod = 'NP_META_10y'
    print(load_raw(mod))







