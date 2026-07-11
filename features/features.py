import matplotlib
matplotlib.use("module://matplotlib-backend-kitty")



def add_net_profit(raw_data):
    raw_data["Net"] = raw_data["Close"] - raw_data["Open"]
    raw_data["Profit"] = raw_data["Net"] > 0
    return raw_data


def add_return(df):
    df["Return"] = df["Close"].pct_change()
    return df


def add_rolling(mod1, time_span):
    mod1["Rolling"] = mod1["Close"].rolling(window=time_span).mean()
    return mod1


def add_volatility(df, rolling):
    df["Volatility"] = df["Close"].rolling(window=rolling).std()
    return df
