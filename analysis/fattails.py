import matplotlib
matplotlib.use("module://matplotlib-backend-kitty")
import matplotlib.pyplot as plt
import numpy as np
import scipy
import seaborn as sns



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


def plot_histogram(df, size_of_df):
    return plt.hist(df["Return"], bins=size_of_df, edgecolor="black")


def plot_normal_curve(df):
    mean = df["Return"].mean()
    std = df["Return"].std()
    x = np.linspace(mean - 4 * std, mean + 4 * std, 100)
    # returns y values////when plotting do plt.plot(x, y)
    return (x, scipy.stats.norm.pdf(x, mean, std))


def add_Correlation_matrix(df, columns):
    return df[columns].corr()


def plot_heatmap(matrix):
    return sns.heatmap(matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1)

