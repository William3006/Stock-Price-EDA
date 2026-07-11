import matplotlib
from PIL.ImageFilter import EDGE_ENHANCE_MORE

matplotlib.use("module://matplotlib-backend-kitty")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
import seaborn as sns
import yfinance as yf
from sklearn.ensemble import IsolationForest


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
        ax = plt.gca()
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(12))
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
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
    return scipy.stats.kurtosis(df["Return"].dropna())


def get_skewness(df):
    return scipy.stats.skew(df["Return"].dropna())


def show_fattails(df, size_of_df):
    plot_histogram(df, size_of_df)
    x, y = plot_normal_curve(df)
    plt.plot(x, y)
    kurt_val = get_kurtosis(df)
    skew_val = get_skewness(df)
    plt.annotate(f"Kurtosis: {kurt_val:.4f}", xy=(0.05, 0.95), xycoords="axes fraction")
    plt.annotate(f"Skewness: {skew_val:.4f}", xy=(0.80, 0.95), xycoords="axes fraction")
    plt.show()


def show_candle_stick(df):
    data_toplot = df[["Open", "Close", "High", "Low"]].copy()
    plt.figure()

    up = data_toplot[data_toplot.Close >= data_toplot.Open]
    down = data_toplot[data_toplot.Close < data_toplot.Open]

    col1 = "green"
    col2 = "red"
    width = 0.3
    width2 = 0.03

    plt.bar(up.index, up.Close - up.Open, width, bottom=up.Open, color=col1)  # body
    plt.bar(
        up.index, up.High - up.Close, width2, bottom=up.Close, color=col1
    )  # upper wick
    plt.bar(up.index, up.Open - up.Low, width2, bottom=up.Low, color=col1)  # lower wick

    plt.bar(
        down.index, down.Open - down.Close, width, bottom=down.Close, color=col2
    )  # body
    plt.bar(
        down.index, down.High - down.Open, width2, bottom=down.Open, color=col2
    )  # upper wick
    plt.bar(
        down.index, down.Close - down.Low, width2, bottom=down.Low, color=col2
    )  # lower wick

    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.show()


def flag_point_outlier(df, show_plot=False):
    # Utilizes IQR
    data = df["Return"]
    window_size = 20
    df["Rolling_q1"] = data.rolling(window=window_size).quantile(0.25)
    df["Rolling_q3"] = data.rolling(window=window_size).quantile(0.75)
    df["Rolling_IQR"] = df["Rolling_q3"] - df["Rolling_q1"]

    k = 1.5
    lower_limit=df["Rolling_q1"] - k * df["Rolling_IQR"]
    upper_limit=df["Rolling_q3"] + k * df["Rolling_IQR"]
    
    df["IQR_flag"] = (data < lower_limit) | (
        data > upper_limit
    )

    if show_plot:
        plot_outlined_data(df, 'IQR_flag', lower_limit, upper_limit)
    return df


def z_flag(df, show_plot=False):
    data = df['Return']
    window_size = 20
    df['Rolling_Mean'] = data.rolling(window=window_size).mean()
    df['Rolling_std'] = data.rolling(window=window_size).std()
    df['Rolling_z'] = (data - df['Rolling_Mean'])/df['Rolling_std']

    threshhold = 3.0

    df['Z_flag'] = df['Rolling_z'].abs() > threshhold 
    if show_plot:
        plot_outlined_data(df, 'Z_flag', None, None)
    return df


def flag_isolation_forest(df, features, show_plot=False):
    #default_features = ['Return', 'Rolling_std', 'Rolling_Mean']
    if features is None:
        features = ['Return', 'Rolling_std', 'Rolling_Mean']
    X = df[features].dropna()
    clf = IsolationForest(contamination=0.05, random_state=42)
    X['IF_flag'] = clf.fit_predict(X) == -1  # -1 = outlier, 1 = normal
    
    df['IF_flag'] = X['IF_flag']
    df['IF_flag'] = df['IF_flag'].fillna(False)
    
    if show_plot:
        plot_outlined_data(df, 'IF_flag', None, None)
    return df
    

def anamoly_detection(df, features=None, combined_plot=False, show_individual_plot=False):
    df = flag_point_outlier(df, show_individual_plot)
    df = z_flag(df, show_individual_plot)
    df = flag_isolation_forest(df, features, show_individual_plot)
    
    df['Flag_count'] = df['IQR_flag'].astype(int) + df['Z_flag'].astype(int) + df['IF_flag'].astype(int)
    df['Flagged'] = df['Flag_count'] >= 2
    
    if combined_plot:
        plot_outlined_data(df, 'Flagged', None, None)
    
    return df


def drawdown_analysis(df, show_plot=False):
    data = df['Close']

    df['max_cumclosing'] = data.cummax()
    df['Drawdown'] = (data - df['max_cumclosing'])/df['max_cumclosing']
    if show_plot:
        plot(df, ['Drawdown'], 0, 2515)
        
    return df

def plot_outlined_data(df, Bool_Flag, lower_limit_axis, upper_limit_axis):
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(df.index, df['Return'], color='steelblue', linewidth=0.8, label='Return')
    if lower_limit_axis is not None:
        ax.plot(df.index, lower_limit_axis, color='gray', linewidth=0.6, linestyle='--', label='Lower fence')
    if upper_limit_axis is not None:
        ax.plot(df.index, upper_limit_axis, color='gray', linewidth=0.6, linestyle='--', label='Upper fence')
    flagged = df[df[Bool_Flag]]
    ax.scatter(flagged.index, flagged['Return'], color='red', s=20, zorder=5, label='Outlier')
    ax.set_title(f'Return outliers ({Bool_Flag})')
    ax.set_xlabel('Date')
    ax.set_ylabel('Return')
    ax.legend()
    ax = plt.gca()
    ax.xaxis.set_major_locator(plt.MaxNLocator(12))  # ~one per year
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # testing load function
    mod = load_raw("NP_META_10y")
    #print(mod.index)
    #anamoly_detection(mod, combined_plot=True)
    #Testing for a differnt ticker, hope it works...


    mod2 = load_new("AAPL", "10y")
    add_return(mod2)
    add_rolling(mod2, 20)
    add_volatility(mod2, 20)
    anamoly_detection(mod2, combined_plot=True)
    drawdown_analysis(mod2, show_plot=True)
    show_fattails(mod2, 50)
    # save(mod, 'NP_META_10y')
    # print(mod)
