import matplotlib
from PIL.ImageFilter import EDGE_ENHANCE_MORE

matplotlib.use("module://matplotlib-backend-kitty")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
import seaborn as sns
import yfinance as yf


def load_new(Name_of_stock, Period):
    ticker = yf.Ticker(Name_of_stock)
    data = ticker.history(period=Period)
    return pd.DataFrame(data)


def load_raw(name, i=None, j=None):
    if i is None or j is None:
        return pd.read_csv(f"csv_saves/{name}.csv")

    return pd.read_csv(f"csv_saves/{name}.csv", skiprows=i, nrows=j)


def save(df, name):
    df.to_csv(f"csv_saves/{name}.csv", index=False)
    print(f"Saved Successfully to csv_saves/{name}.csv!")


def add_net_profit(raw_data):
    raw_data["Net"] = raw_data["Close"] - raw_data["Open"]
    raw_data["Profit"] = raw_data["Net"] > 0
    return raw_data


def add_return(df):
    df["Return"] = df["Close"].pct_change()


def add_rolling(mod1, time_span):
    mod1["Rolling"] = mod1["Close"].rolling(window=time_span).mean()
    return mod1


# just realised there's a built in pandas that does this for me and it uses Bessel's correction😭😭😭


def add_volatility(df, rolling):
    df["Volatility"] = df["Close"].rolling(window=rolling).std()
    return df


"""
def add_volatility(df, rolling):
    df['diff']=(df['Close']-df['Rolling'])**2
    df['roll_diff']=df['diff'].rolling(window=rolling).sum()
    df['Volatility']=np.sqrt((df['roll_diff']/rolling))

    df=df.drop(columns=['diff', 'roll_diff'])

    return df
    """
# For my current setting of running the code from terminal in Arch, the plt.show method does not work, hence working around it using Agg
# Using kitty to view image plots in terminal!!!


def plot(df, columns, i, j):
    subset_df = df[columns].iloc[i:j]

    for col in columns:
        plt.plot(subset_df.index, subset_df[col], label=col)

    plt.title("Data points visualised")
    plt.xlabel("Date")
    plt.ylabel(columns)
    plt.legend()
    plt.grid(True)

    print("Do you want to save this plot?(y/n)")
    save_parameter = input()
    if save_parameter == "y":
        save_name = input("Enter image name: ")
        plt.savefig(f"Meta_Plots/{save_name}.png")

    plt.show()

    print(
        "!!![WARNING]!!! Make sure data is scaled before using, entities such as volume are off scale compared to the others."
    )


def add_Correlation_matrix(df, columns):
    return df[columns].corr()


def plot_heatmap(matrix):
    return sns.heatmap(matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1)


def plot_histogram(df, size_of_df):
    return plt.hist(df["Return"], bins=size_of_df, edgecolor="black")


def plot_normal_curve(df):
    mean = df["Return"].mean()
    std = df["Return"].std()
    x = np.linspace(mean - 4 * std, mean + 4 * std, 100)
    # returns y values////when plotting do plt.plot(x, y)
    return (x, scipy.stats.norm.pdf(x, mean, std))


def get_kurtosis(df):
    return scipy.stats.kurtosis(df['Return'].dropna())


def get_skewness(df):
    return scipy.stats.skew(df['Return'].dropna())


def show_fattails(df, size_of_df):
    plot_histogram(df, size_of_df)
    x, y = plot_normal_curve(df)
    plt.plot(x, y)
    kurt_val = get_kurtosis(df)
    skew_val = get_skewness(df)
    plt.annotate(f'Kurtosis: {kurt_val:.4f}', xy=(0.05, 0.95), xycoords='axes fraction')
    plt.annotate(f'Skewness: {skew_val:.4f}', xy=(0.80, 0.95), xycoords='axes fraction')
    plt.show()



if __name__ == "__main__":
    # testing load function
    mod = load_raw("NP_META_10y")
    show_fattails(mod, 2515)

    # save(mod, 'NP_META_10y')
    #print(mod)
