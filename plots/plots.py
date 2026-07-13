import matplotlib
import sys
if sys.platform == 'linux':
    matplotlib.use("module://matplotlib-backend-kitty")
import matplotlib.pyplot as plt



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